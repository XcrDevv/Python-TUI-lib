from tui.app import gen_id
from tui.commands import command
from tui.messages import Msg
from tui.messages import KeyPressMsg
from tui.utils import SupportsStr
from typing import Sequence, TypeVar, Generic
from dataclasses import dataclass

@dataclass
class SelectFocusMsg:
    id: int
    
@dataclass
class SelectBlurMsg:
    id: int

T = TypeVar('T', bound=SupportsStr)

class SelectModel(Generic[T]):
    def __init__(self):
        self._id = gen_id()
        self._focus = True # ! <--- True?
        self.options: Sequence[T] = []
        self.selected = 0
        
    def update(self, msg: Msg):
        match msg:
            case KeyPressMsg(key='up') if self._focus:
                self.selected = len(self.options) - 1 if self.selected == 0 else self.selected - 1
            case KeyPressMsg(key='down') if self._focus:
                self.selected = 0 if self.selected == len(self.options) - 1 else self.selected + 1
            case SelectFocusMsg(id=id) if self._id == id:
                self._focus = True
            case SelectBlurMsg(id=id) if self._id == id:
                self._focus = False
    
    def get_option(self) -> T:
        return self.options[self.selected]
    
    def get_option_str(self):
        return str(self.options[self.selected])

    def select(self, option: T) -> bool:
        for (i, o) in enumerate(self.options):
            if o == option:
                self.selected = i
                return True
        return False
    
    def focused(self) -> bool:
        return self._focus
    
    @command
    def focus(self):
        if not self._focus:
            return SelectFocusMsg(self._id)
        
    @command
    def blur(self):
        if self._focus:
            return SelectBlurMsg(self._id)