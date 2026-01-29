from tui.containers import ContainerElement
from tui.element import Element, Rect

class VerticalElement(ContainerElement):
    def __init__(
        self, 
        rect: Rect,
        padding_x: int, 
        padding_y: int,
        border: int,
        rounded: bool,
        elements: list[Element]
    ):
        super().__init__(rect, padding_x, padding_y, border, rounded, elements)