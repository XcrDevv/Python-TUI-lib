from tui.builder import ElementBuilder
from tui.element import Rect
from .element import TextInputElement
from .model import TextInputModel

class TextInput(ElementBuilder):
    def __init__(self, model: TextInputModel):
        super().__init__()
        self._model = model
        self._placeholder = ''
        self._prompt = '>'
        self._pos = 0
        
    def prompt(self, prompt: str):
        self._prompt = prompt
        return self
    
    def value(self, value: str):
        self._value = value
        return self
    
    def placeholder(self, placeholder: str):
        self._placeholder = placeholder
        return self
    
    def build(self):
        width = 1 if self._width is None else self._width
        height = 1 if self._height is None else self._height
        
        rect = Rect(self._x, self._y, width, height)
        
        return TextInputElement(
            rect,
            self._model,
            self._placeholder,
            self._prompt,
        )