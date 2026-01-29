from tui.builder import ElementBuilder
from tui.element import Rect
from tui.utils import wrap_text
from .element import TextElement

class Text(ElementBuilder):
    def __init__(self, text: str = ''):
        super().__init__()
        self.text = text

    def build(self):
        width = len(self.text) if self._width is None else self._width
        height = len(wrap_text(self.text, width))
        rect = Rect(self._x, self._y, width, height)
        
        return TextElement(rect, self.text)