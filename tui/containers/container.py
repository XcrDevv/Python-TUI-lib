from tui.element import Element, Rect
from tui.buffer import TermBuffer

class ContainerElement(Element):
    def __init__(
        self, 
        rect: Rect,
        padding_x: int, 
        padding_y: int,
        border: int,
        rounded: bool,
        elements: list[Element]
    ):
        super().__init__(rect)
        self.padding_x = padding_x
        self.padding_y = padding_y
        self.border = border
        self.rounded = rounded
        
        self.elements = elements
        
        self.filled_space = 0
        
    def draw(self, buffer: TermBuffer):
        if self.border == 1:
            self.draw_border(buffer)
        
        for e in self.elements:
            e.draw(buffer)
            
    def draw_border(self, buffer: TermBuffer):
        lt = '╭' if self.rounded else '┌'
        rt = '╮' if self.rounded else '┐'
        rb = '╯' if self.rounded else '┘'
        lb = '╰' if self.rounded else '└'
        hr = '─'
        vr = '│'
        
        buffer.move_to(self.x, self.y)
        buffer.write(f'{lt}{hr * (self.width - 2)}{rt}')
        for i in range(self.height - 2):
            buffer.move_to(self.x, self.y + i + 1)
            buffer.write(f"{vr}{' ' * (self.width - 2)}{vr}")
        buffer.move_to(self.x, buffer.cursor[1] + 1)
        buffer.write(f'{lb}{hr * (self.width - 2)}{rb}')
        
    def set_border(self, value: bool = True, rounded: bool = False):
        self.rounded = rounded
        self.border = 1 if value else 0
        self.resize()
        
    def set_padding(self, padding: tuple[int, int]):
        self.padding_x = padding[0]
        self.padding_y = padding[1]
        self.resize()