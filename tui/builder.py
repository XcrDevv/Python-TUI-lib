from .element import Element
from abc import ABC, abstractmethod

class ElementBuilder(ABC):
    def __init__(self):
        self._width = None
        self._height = None
        self._x = 0
        self._y = 0
    
    def width(self, width: int):
        self._width = width
        return self
    
    def height(self, height: int):
        self._height = height
        return self
    
    def x(self, x: int):
        self._x = x
        return self
    
    def y(self, y: int):
        self._y = y
        return self
    
    @abstractmethod
    def build(self) -> Element:...