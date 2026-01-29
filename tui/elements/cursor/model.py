from tui.messages import Msg
from tui.commands import Cmd, tick, command
from tui.app import gen_id
from dataclasses import dataclass

@dataclass(frozen=True)
class CursorStartBlinkMsg:
    id: int
    
@dataclass(frozen=True)
class CursorTickMsg:
    id: int
    gen: int
    
@dataclass(frozen=True)
class CursorStopBlinkMsg:
    id: int

class CursorModel:
    def __init__(self):
        self._id = gen_id()
        self._focused = False
        self._anchor = 0
        self._displacement = 0
        self._blink_gen = 0
        self._blink_cursor = False
        
    @property
    def pos(self):
        return (self._anchor, self._displacement)
    
    @property
    def blink(self):
        return self._blink_cursor
    
    def has_selection(self):
        return self._anchor != self._displacement
    
    def set_to(self, value: int):
        self._anchor = value
        self._displacement = value
    
    def set_anchor(self, value: int):
        self._anchor = value
        
    def set_displacement(self, value: int):
        self._displacement = value
        
    def offset(self, ammount: int):
        self._anchor += ammount
        self._displacement += ammount
        
    def offset_anchor(self, ammount: int):
        self._anchor += ammount
        
    def offset_displacement(self, ammount: int):
        self._displacement += ammount
    
    def rst_blink(self):
        self._blink_cursor = True
        
    def update(self, msg: Msg) -> Cmd | None:
        match msg:
            case CursorStartBlinkMsg(id=self._id):
                self.set_to(max(self.pos)) # just to clear any selection
                self._focused = True
                self._blink_cursor = True
                self._blink_gen += 1
                gen = self._blink_gen
                return tick(0.5, lambda: CursorTickMsg(self._id, gen))
            
            case CursorStopBlinkMsg(id=self._id):
                self._focused = False
                self._blink_cursor = False
                
            case CursorTickMsg(id=self._id, gen=gen) if gen == self._blink_gen:
                if not self._focused:
                    return None 
                
                self._blink_cursor = not self._blink_cursor
                return tick(0.5, lambda: CursorTickMsg(self._id, gen))
        return None
    
    def focused(self) -> bool:
        return self._focused
    
    @command
    def focus(self) -> Msg:
        if not self._focused:
            return CursorStartBlinkMsg(self._id)
        
    @command
    def blur(self):
        if self._focused:
            return CursorStopBlinkMsg(self._id)