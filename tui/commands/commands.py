from tui.messages import *
from typing import List, Iterator, Callable, Any
from datetime import datetime
from functools import wraps
import inspect
import asyncio
import time

Cmd = Callable[[], Msg]
Model = Any

def command(func: Callable[..., Msg]) -> Callable[..., Callable[[], Msg]]:
    sig = inspect.signature(func)
    params = list(sig.parameters.values())
    
    is_method = len(params) > 0 and params[0].name in ('self')
    
    if is_method:
        # Wrapper for methods
        @wraps(func)
        def method_wrapper(self: Any, *args: Any, **kwargs: Any) -> Callable[[], Msg]:
            def command_thunk() -> Msg:
                return func(self, *args, **kwargs)
            return command_thunk
        return method_wrapper
    else:
        # Wrapper for normal functions
        @wraps(func)
        def function_wrapper(*args: Any, **kwargs: Any) -> Callable[..., Msg]:
            def command_thunk() -> Msg:
                return func(*args, **kwargs)
            return command_thunk
        return function_wrapper

class Cmds:
    def __init__(self):
        self._cmds: List[Cmd] = []
        
    def perform(self, cmd: Cmd | None):
        if cmd is not None:
            self._cmds.append(cmd)
        
    def batch(self, *cmds: Cmd):
        self._cmds.append(batch(*cmds))
        
    def sequence(self, *cmds: Cmd):
        self._cmds.append(sequence(*cmds))
    
    def __iter__(self) -> Iterator[Cmd]:
        return iter(self._cmds)

@command
def quit() -> Msg:
    return QuitMsg()

def tick(duration: int | float, fn: Callable[..., Any]) -> Cmd:
    async def _tick():
        await asyncio.sleep(duration)
        if asyncio.iscoroutinefunction(fn):
            return await fn()
        else: 
            return await asyncio.to_thread(fn)
    return _tick

@command
def clear() -> Msg:
    return ClearMsg()

def every(duration: int | float, fn: Callable[..., Any]) -> Cmd:
    now = time.time()
    next_tick = ((now // duration) + 1) * duration
    delay = next_tick - now

    async def _every():
        await asyncio.sleep(delay)
        ts = datetime.fromtimestamp(next_tick)

        if asyncio.iscoroutinefunction(fn):
            return await fn(ts)
        else:
            return await asyncio.to_thread(fn)

    return _every

def batch(*cmds: Cmd) -> Cmd:
    async def _batch():
        valid_cmds = [cmd for cmd in cmds if cmd is not None]

        if not valid_cmds:
            return None

        if len(valid_cmds) == 1:
            return await valid_cmds[0]() if asyncio.iscoroutinefunction(valid_cmds[0]) \
                else await asyncio.to_thread(valid_cmds[0])

        return ExecBatchMsg(cmds=valid_cmds)
    
    return _batch

def sequence(*cmds: Cmd) -> Cmd:
    async def _sequence():
        valid_cmds = [cmd for cmd in cmds if cmd is not None]

        if not valid_cmds:
            return None

        if len(valid_cmds) == 1:
            return await valid_cmds[0]() if asyncio.iscoroutinefunction(valid_cmds[0]) \
                else await asyncio.to_thread(valid_cmds[0])

        return ExecSequenceMsg(cmds=valid_cmds)

    return _sequence