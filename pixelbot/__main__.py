import logging
import sys
from argparse import ArgumentParser
from contextlib import contextmanager

import glfw
from OpenGL import GL
from skia import ColorSpace
from skia import GrBackendRenderTarget
from skia import GrDirectContext
from skia import GrGLFramebufferInfo
from skia import Rect
from skia import Surface
from skia import kBottomLeft_GrSurfaceOrigin
from skia import kRGBA_8888_ColorType

from pixelbot.config import load_config
from pixelbot.services.manager import ServiceManager
from pixelbot.ui.backends.skia.context import Context
from pixelbot.ui.backends.skia.renderer_skia import SkiaRenderer
from pixelbot.widgets.base import Widget
from pixelbot.widgets.loader import load_widget

log = logging.getLogger("pixelbot.__main__")


def main(argv: list[str] = None):
    logging.basicConfig(level=logging.DEBUG)
    log.info("Starting PixelBot")

    argparse = ArgumentParser()
    argparse.add_argument("--debug", action="store_true", help="Enable debug mode")
    argparse.add_argument(
        "--fullscreen", action="store_true", help="Start in fullscreen mode"
    )
    args = argparse.parse_args(argv)

    config = load_config()

    manager = ServiceManager()
    manager.load(config["services"])
    widget = load_widget(config["widget"], manager)
    manager.start()

    run_skia(widget, args.debug, args.fullscreen)

    manager.stop()


WIDTH, HEIGHT = 1024, 600


@contextmanager
def glfw_window(fullscreen: bool):
    if not glfw.init():
        raise RuntimeError("glfw.init() failed")
    glfw.window_hint(glfw.STENCIL_BITS, 8)

    if fullscreen:
        monitor = glfw.get_primary_monitor()
    else:
        monitor = None

    window = glfw.create_window(WIDTH, HEIGHT, "Pixelbot", monitor, None)

    glfw.make_context_current(window)
    yield window
    glfw.destroy_window(window)
    glfw.terminate()


@contextmanager
def skia_surface(window):
    context = GrDirectContext.MakeGL()
    (fb_width, fb_height) = glfw.get_framebuffer_size(window)
    backend_render_target = GrBackendRenderTarget(
        fb_width,
        fb_height,
        0,  # sampleCnt
        0,  # stencilBits
        GrGLFramebufferInfo(0, GL.GL_RGBA8),
    )
    surface = Surface.MakeFromBackendRenderTarget(
        context,
        backend_render_target,
        kBottomLeft_GrSurfaceOrigin,
        kRGBA_8888_ColorType,
        ColorSpace.MakeSRGB(),
    )
    assert surface is not None
    yield surface
    context.abandonContext()


def run_skia(widget: Widget, debug: bool, fullscreen: bool):
    with glfw_window(fullscreen) as window:
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        with skia_surface(window) as surface:
            with surface as canvas:
                renderer = SkiaRenderer(
                    Context(
                        screen_width=WIDTH,
                        screen_height=HEIGHT,
                        actual_width=surface.width(),
                        actual_height=surface.height(),
                        debug=debug,
                    )
                )

                def _render():
                    renderer.render(
                        canvas, widget, Rect(0, 0, surface.width(), surface.height())
                    )
                    surface.flushAndSubmit()
                    glfw.swap_buffers(window)

                _render()

                while glfw.get_key(
                    window, glfw.KEY_ESCAPE
                ) != glfw.PRESS and not glfw.window_should_close(window):
                    if widget.update_interval > 0:
                        glfw.wait_events_timeout(widget.update_interval / 1000)
                        _render()
                    else:
                        glfw.wait_events()


if __name__ == "__main__":
    main(sys.argv[1:])
