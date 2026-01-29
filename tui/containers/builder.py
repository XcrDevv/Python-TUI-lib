from tui.builder import ElementBuilder
from tui.element import Element, Rect
from tui.containers.horizontal import HorizontalElement
from tui.containers.vertical import VerticalElement
from typing import Iterable, List, cast
import os

class Container(ElementBuilder):
    def __init__(self):
        self._x = 0
        self._y = 0
        self._width = 0
        self._height = 0
        self._padding_x = 0
        self._padding_y = 0
        self._border = 0
        self._rounded = False
        self._elements: List[ElementBuilder] = []
        
    def vertical(self):
        self._type = 'vertical'
        return self
    
    def horizontal(self):
        self._type = 'horizontal'
        return self
    
    def width(self, width: int | None):
        self._width = width
        return self
    
    def height(self, height: int | None):
        self._height = height
        return self
    
    def size(self, width: int | None, height: int | None):
        self._width = width
        self._height = height
        return self
    
    def padding(self, padding_x: int, padding_y: int):
        self._padding_x = padding_x
        self._padding_y = padding_y
        return self
    
    def border(self, rounded: bool = False):
        self._border = 1
        self._rounded = rounded
        return self
    
    def add(self, element: ElementBuilder):
        self._elements.append(element)
        return self
    
    def set(self, elements: Iterable[ElementBuilder]):
        self._elements = cast(List[ElementBuilder], elements)
        return self
        
    def build(self):
        width = os.get_terminal_size().columns if self._width is None else self._width
        rect = Rect(self._x, self._y, width, 0)
        
        params = (
            rect,
            self._padding_x,
            self._padding_y,
            self._border,
            self._rounded,
        )
        
        if self._type == 'vertical':
            built_elements: List[Element] = []
            filled_space = 0
            
            for e in self._elements:
                if not e._width:
                    e._width = (os.get_terminal_size().columns)
                
                if e._y == 0:
                    e._y = self._y + filled_space
                        
                new_element = e.build()
                filled_space += new_element.height
                built_elements.append(new_element)
            
            return VerticalElement(*params, built_elements)
        else:
            built_elements: List[Element] = []
            filled_space = 0

            for e in self._elements:
                if not e._height:
                    e._height = os.get_terminal_size().lines

                if e._x == 0:
                    e._x = filled_space
                    
                e._y = self._y

                new_element = e.build()
                filled_space += new_element.width
                built_elements.append(new_element)

            return HorizontalElement(*params, built_elements)