from .buffer import TermBuffer
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Rect:
    x: int
    y: int
    width: int
    height: int

class Element(ABC):
    def __init__(self, rect: Rect):
        self.rect = rect
        
    @property
    def x(self):
        return self.rect.x
    
    @property
    def y(self):
        return self.rect.y
    
    @property
    def width(self):
        return self.rect.width
    
    @property
    def height(self):
        return self.rect.height
        
    @abstractmethod
    def draw(self, buffer: TermBuffer) -> None:...
    
    def resize(self) -> None:...
    
    def set_size(self, width: int, height: int):
        self.rect.width = width
        self.rect.height = height
        self.resize()
        
    def set_position(self, x: int, y: int):
        self.rect.x = x
        self.rect.y = y
