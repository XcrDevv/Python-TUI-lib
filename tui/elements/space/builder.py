from tui.builder import ElementBuilder
from tui.element import Rect
from .element import SpaceElement

class Space(ElementBuilder):
    def __init__(self, width: int = 1, height: int = 1):
        super().__init__()
        self._height = width
        self._width = height
    
    def build(self):
        rect = Rect(0, 0, self._width, self._height)
        return SpaceElement(rect)