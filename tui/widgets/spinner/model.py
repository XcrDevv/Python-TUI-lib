from tui.messages import Msg
from tui.commands import tick, command
from tui.app import gen_id
from dataclasses import dataclass

SPINNERS = {
    'line': ['|', '/', '-', '\\'],
    'dot': ['⣾ ', '⣽ ', '⣻ ', '⢿ ', '⡿ ', '⣟ ', '⣯ ', '⣷ '],
    'minidot': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
    'jump': ['⢄', '⢂', '⢁', '⡁', '⡈', '⡐', '⡠'],
    'pulse': ['█', '▓', '▒', '░'],
    'points': ['∙∙∙', '●∙∙', '∙●∙', '∙∙●'],
    'ellipsis': ['   ', '.  ', '.. ', '...'],
    'block': ['▖', '▘', '▝', '▗'],
    'bar': ['▁','▃','▄','▅','▆','▇','█','▇','▆','▅','▄','▃']
}

@dataclass(frozen=True)
class SpinnerTickMsg:
    id: int

@dataclass(frozen=True)
class SpinnerStartMsg:
    id: int

@dataclass(frozen=True)
class SpinnerStopMsg:
    id: int

class SpinnerModel:
    def __init__(self):
        self._id = gen_id()
        self.frames = SPINNERS['line']
        self.frame = 0
        self.running = False
        
    def set_frames(self, frames: list[str]):
        self.frames = frames
        
    def update(self, msg: Msg):
        match msg:
            case SpinnerStartMsg(id=self._id):
                self.running = True
                return tick(0.12, lambda: SpinnerTickMsg(self._id))
            case SpinnerStopMsg(id=self._id):
                self.running = False
                return None
            case SpinnerTickMsg(id=self._id) if self.running:
                self.frame = (self.frame + 1) % len(self.frames)
                return tick(0.12, lambda: SpinnerTickMsg(self._id))
            
        return None
    
    @command
    def start(self) -> Msg:
        return SpinnerStartMsg(self._id)
    
    @command
    def stop(self) -> Msg:
        return SpinnerStopMsg(self._id)