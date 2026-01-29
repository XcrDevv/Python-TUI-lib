from tui.builder import ElementBuilder
from tui.element import Rect
from .element import SelectElement
from .model import SelectModel
from typing import Any

class Select(ElementBuilder):
    def __init__(self, model: SelectModel[Any]):
        super().__init__()
        self._model = model
        self._prompt = ''
        self._rows = None
        
    def prompt(self, text: str):
        self._prompt = text
        return self
    
    def rows(self, number: int):
        self._rows = number
        return self
    
    def build(self):
        rect = Rect(self._x, self._y, 1, len(self._model.options) + 2)
        
        return SelectElement(
            rect,
            self._model,
            self._prompt,
            self._rows,
        )