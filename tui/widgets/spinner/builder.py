from tui.element import Rect
from tui.builder import ElementBuilder
from .model import SpinnerModel
from .element import SpinnerElement

class Spinner(ElementBuilder):
    def __init__(self, model: SpinnerModel):
        super().__init__()
        self._model = model
        self._color = None
        
    def color(self, color: str):
        self._color = color
        return self
    
    def build(self):
        rect = Rect(self._x, self._y, len(self._model.frames[0]), 1)
        
        return SpinnerElement(
            rect,
            self._model,
            self._color,
        )