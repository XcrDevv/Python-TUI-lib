from tui.messages import *
from typing import List, Iterator, Callable, Any
from datetime import datetime
from functools import wraps
import inspect
import asyncio
import time
from functools import wraps
from typing import Callable, Awaitable, TypeVar, ParamSpec, Union

Cmd = Callable[[], Msg]
Model = Any

P = ParamSpec("P")
R = TypeVar("R", bound="Msg")

Thunk = Callable[[], Union[R, Awaitable[R]]]

def command(func: Callable[P, R] | Callable[P, Awaitable[R]]) -> Callable[P, Thunk[R]]:
    is_async = inspect.iscoroutinefunction(func)

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Thunk[R]:

        async def async_thunk() -> R:
            return await func(*args, **kwargs)  # type: ignore

        def sync_thunk() -> R:
            return func(*args, **kwargs)  # type: ignore

        thunk: Thunk[R] = async_thunk if is_async else sync_thunk
        return thunk

    return wrapper

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
        if inspect.iscoroutinefunction(fn):
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

        if inspect.iscoroutinefunction(fn):
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
            return await valid_cmds[0]() if inspect.iscoroutinefunction(valid_cmds[0]) \
                else await asyncio.to_thread(valid_cmds[0])

        return ExecBatchMsg(cmds=valid_cmds)
    
    return _batch

def sequence(*cmds: Cmd) -> Cmd:
    async def _sequence():
        valid_cmds = [cmd for cmd in cmds if cmd is not None]

        if not valid_cmds:
            return None

        if len(valid_cmds) == 1:
            return await valid_cmds[0]() if inspect.iscoroutinefunction(valid_cmds[0]) \
                else await asyncio.to_thread(valid_cmds[0])

        return ExecSequenceMsg(cmds=valid_cmds)

    return _sequence