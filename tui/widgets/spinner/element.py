from tui.element import Element, Rect
from tui.buffer import TermBuffer
from tui.colors import colored
from .model import SpinnerModel

class SpinnerElement(Element):
    def __init__(
        self, 
        rect: Rect,
        model: SpinnerModel,
        color: str | None = None
    ):
        super().__init__(rect)
        self.model = model
        self.color = color

    def draw(self, buffer: TermBuffer):
        buffer.move_to(self.x, self.y)
        if self.color is not None:
            buffer.write(colored(self.model.frames[self.model.frame], self.color))
        else:
            buffer.write(self.model.frames[self.model.frame])