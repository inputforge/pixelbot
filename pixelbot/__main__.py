import logging
import sys

from wx import EVT_CLOSE
from wx import EVT_TIMER
from wx import Frame
from wx import Timer

from pixelbot.app import PixelBotApp
from pixelbot.config import load_config
from pixelbot.services.manager import ServiceManager
from pixelbot.widgets.loader import load_widget
from pixelbot.widgets.renderer import Renderer

log = logging.getLogger(__name__)


def main(args: list[str] = None):
    logging.basicConfig(level=logging.DEBUG)

    log.info("Starting PixelBot")

    config = load_config()

    manager = ServiceManager()
    manager.load(config["services"])

    app = PixelBotApp()
    frame = Frame(parent=None, title="PixelBot")

    if args and args[0] == "--fullscreen":
        frame.ShowFullScreen(True)
    else:
        frame.SetSize((1024, 600))

    renderer = Renderer()
    widget = load_widget(config["widget"], manager)
    renderer.render(frame, widget)

    if widget.update_interval:
        print("Starting timer")
        app.timer = Timer(frame)
        frame.Bind(EVT_TIMER, lambda _: renderer.update())
        app.timer.Start(widget.update_interval)

    def on_close(*_, **__):
        log.info("Closing PixelBot")
        frame.Destroy()
        manager.stop()
        app.ExitMainLoop()

    frame.Bind(EVT_CLOSE, on_close)

    manager.start()

    frame.Show()
    app.MainLoop()
    log.info("PixelBot shutdown")


if __name__ == "__main__":
    main(sys.argv[1:])
