from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass


@dataclass
class Context:
    screen_width: int
    screen_height: int
    actual_width: int
    actual_height: int
    debug: bool = False

    device = "PixelBot"
    color_mode = "RGB_888"

    @property
    def dppx(self) -> float:
        return self.actual_width / self.screen_width


current_ctx: ContextVar[Context] = ContextVar("current_context")


@contextmanager
def context(ctx: Context):
    token = current_ctx.set(ctx)
    yield
    current_ctx.reset(token)


def current_context() -> Context:
    return current_ctx.get()
