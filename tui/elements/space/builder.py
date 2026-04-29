from tui.builder import ElementBuilder
from tui.element import Rect
from .element import SpaceElement

class Space(ElementBuilder):
    def __init__(self, vertical: int = 1, horizontal: int = 1):
        super().__init__()
        self._width = horizontal
        self._height = vertical
    
    def build(self):
        rect = Rect(0, 0, self._width, self._height)
        return SpaceElement(rect)