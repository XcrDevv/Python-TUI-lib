from dataclasses import dataclass
from typing import Any, List

Msg = Any

class InternalMsg: pass

class StartMsg(InternalMsg): pass

class QuitMsg(InternalMsg): pass

@dataclass(frozen=True)
class KeyPressMsg(InternalMsg):
    key: str
    
class TickMsg(InternalMsg): pass

class ClearMsg(InternalMsg): pass

@dataclass(frozen=True)
class ExecBatchMsg(InternalMsg):
    cmds: List[Msg]
    
@dataclass(frozen=True)
class ExecSequenceMsg(InternalMsg):
    cmds: List[Msg]
