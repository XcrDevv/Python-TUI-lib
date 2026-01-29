from tui.builder import ElementBuilder
from tui.element import Rect
from .element import SpaceElement

class Space(ElementBuilder):
    def __init__(self):
        super().__init__()
        self._height = 1
        self._width = 1
    
    def build(self):
        rect = Rect(0, 0, 1, 1)
        return SpaceElement(rect)