from tui.builder import ElementBuilder
from tui.element import Rect
from .model import ProgressModel
from .element import ProgessElement

class Progress(ElementBuilder):
    def __init__(self, model: ProgressModel):
        super().__init__()
        self._model = model

    def build(self):
        width = 30 if self._width is None else self._width
        rect = Rect(self._x, self._y, width, 1)
        
        return ProgessElement(
            rect,
            self._model,
        )    