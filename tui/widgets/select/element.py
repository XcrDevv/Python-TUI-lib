from tui.element import Element, Rect
from tui.buffer import TermBuffer
from tui.colors import colored, bold
from .model import SelectModel
from typing import Any

class SelectElement(Element):
    def __init__(
        self,
        rect: Rect,
        model: SelectModel[Any],
        prompt: str,
        rows: int | None,
    ):
        super().__init__(rect)
        self.model = model
        self.prompt = prompt
        self.rows = rows
        
    def draw(self, buffer: TermBuffer):
        buffer.move_to(self.x, self.y)
        buffer.write(f'{self.prompt}')

        total = len(self.model.options)        
        rows = self.rows if self.rows else total
        
        start = self.model.selected - rows // 2
        start = max(0, min(start, start, total - rows))
        
        for i in range(start, start + rows):
            if not i < total:
                break
            s = self.model.options[i]
            buffer.move_to(self.x, self.y + i + 2 - start)
            if i == self.model.selected and self.model.focused():
                buffer.write(f"{colored('>', 'magenta')} {bold(str(s))}")
            else:
                buffer.write(f'  {s}')