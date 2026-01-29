from tui.element import Element, Rect
from tui.buffer import TermBuffer

class SpaceElement(Element):
    def __init__(self, rect: Rect):
        super().__init__(rect)
        
    def draw(self, buffer: TermBuffer):
        pass

    def get_height(self):
        return self.height
    
    def get_width(self):
        return self.width