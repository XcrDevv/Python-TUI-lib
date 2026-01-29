from tui.element import Element, Rect
from tui.buffer import TermBuffer
from tui.colors import colored
from .model import ProgressModel

class ProgessElement(Element):
    def __init__(
        self,
        rect: Rect,
        model: ProgressModel,
    ):
        super().__init__(rect)
        self.model = model
        
    def draw(self, buffer: TermBuffer):
        progress_bar = ''
        progress_bar_left = ''
        progress_reached = False
        
        for i in range(self.width):
            if i / self.width < self.model.percentage / 100:
                progress_bar += '━'
            else:
                if progress_reached:
                    progress_bar_left += '━'
                else:
                    progress_bar_left += '╺'
                progress_reached = True
        buffer.move_to(self.x, self.y)
        buffer.write(f"[{colored(progress_bar, 'green')}{colored(progress_bar_left, 'red')}]({round(self.model.percentage, 1)}%)")
    