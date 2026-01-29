from tui.element import Element, Rect
from tui.buffer import TermBuffer
from tui.utils import wrap_text

class TextElement(Element):
    def __init__(self, rect: Rect, text: str):
        super().__init__(rect)
        self.text = text
        
    def draw(self, buffer: TermBuffer):
        buffer.move_to(self.x, self.y)
        buffer.write(self.text)
            
    def get_height(self):
        if not self.text:
            return 1
        
        return len(wrap_text(self.text, self.rect.width))
    
    def get_width(self):
        return len(self.text)