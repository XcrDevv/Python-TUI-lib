from tui.element import Element, Rect
from tui.buffer import TermBuffer
from tui.colors import *
from tui.utils import raw_str
from .model import TextInputModel

class TextInputElement(Element):
    def __init__(
        self, 
        rect: Rect,
        model: TextInputModel,
        placeholder: str,
        prompt: str,
    ):
        super().__init__(rect)
        self.model = model
        self.placeholder = placeholder
        self.prompt = prompt
        
    def draw(self, buffer: TermBuffer):
        buffer.move_to(self.x, self.y)
        prompt = colored(self.prompt, 'yellow') if self.model.focused() else colored(self.prompt, 'gray')
        
        if self.model.cursor.has_selection() and self.model.focused():
            start = min(self.model.cursor.pos)
            end = max(self.model.cursor.pos)
            
            pre = self.model.value[:start]
            selected = background(self.model.value[start:end], 'white')
            post = self.model.value[end:]
            buffer.write(f'{prompt} {pre}{selected}{post}')
            return
        
        text = ''
        
        if not self.model.value:
            text += gray(self.placeholder)
        else:
            text += self.model.value
            
        suggestion = gray(self.model.current_suggestion.removeprefix(self.model.value))
        text += suggestion
        
        buffer.write(f'{prompt} {text}')
        
        if self.model.cursor.blink:
            cursor_x = self.x + 2 + self.model.cursor.pos[0]
            cursor_y = self.y
            
            raw = raw_str(text)
            if self.model.cursor.pos[0] > len(raw) - 1:
                buffer.move_to(cursor_x, cursor_y)
                buffer.write('█')
            else:
                buffer.add_style_to_char(cursor_x, cursor_y, '\033[47m')