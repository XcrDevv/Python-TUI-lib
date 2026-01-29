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
    
    def width(self, width: int):
        self._width = width
        return self
    
    def height(self, height: int):
        self._height = height
        return self
    
    def build(self):
        rect = Rect(self._x, self._y, 1, 1)
        
        return TextInputElement(
            rect,
            self._model,
            self._placeholder,
            self._prompt,
        )