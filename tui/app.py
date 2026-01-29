from tui.builder import ElementBuilder
from tui.commands import *
from tui.messages import *
from tui.containers import Container
from tui.buffer import TermBuffer
from tui.key import key_to_string
from typing import Iterable, Any, Callable
from abc import ABC, abstractmethod
from colorama import init # pyright: ignore
from prompt_toolkit.input import create_input
import sys
import os
import asyncio
import threading

Model = Any

_id_count = 0
_id_lock = threading.Lock()

def gen_id() -> int:
    with _id_lock:
        global _id_count
        _id_count += 1
        return _id_count

def main(func: Any) -> Callable[..., Any]:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return asyncio.run(func(*args, **kwargs))
    return wrapper

class App(ABC):
    def __init__(self):
        # enable ansi on windows cmd
        init()
        
        # buffer for rendering
        self._tb = TermBuffer()
    
        self._elements = []
        
        self._running = True
        
        self.msg_queue: asyncio.Queue[Any] = asyncio.Queue()
       
    def init_model(self, *args: Any, **kargs: Any) -> Cmd | None:
        return None
    
    @abstractmethod
    def update(self, msg: Any) -> Cmd | None:...
    
    @abstractmethod
    def view(self) -> Iterable[ElementBuilder]:...
    
    @main
    async def run(self):
        self._input_task_handle = asyncio.create_task(self._input_task())
        
        await self.msg_queue.put(StartMsg())
        
        cmd = self.init_model()
        if cmd is not None:
            await self._execute_cmd(cmd)
        
        self._hide_cursor()
        os.system('cls')
        
        try:
            await self._event_loop()
        finally:
            self._input_task_handle.cancel()
            try:
                await self._input_task_handle
            except asyncio.CancelledError:
                pass
        
        self._show_cursor()
        
    def should_close(self):
        return not self._running
        
    def _quit(self):
        self._running = False
        
        self._tb.clear_deep()
        
        view = Container() \
            .vertical() \
            .set(self.view())
                
        self._draw(view)
        
    async def _event_loop(self):
        while True:
            msg = await self.msg_queue.get()
            
            if msg is None:
                continue
            
            match msg:
                case QuitMsg():
                    self._quit()
                    return
                case ClearMsg():
                    os.system('cls')
                    self._tb.clear()
                case ExecBatchMsg(cmds=cmds):
                    for cmd in cmds:
                        asyncio.create_task(self._execute_cmd(cmd))
                case ExecSequenceMsg(cmds=cmds):
                    for cmd in cmds:
                        await self._execute_cmd(cmd)
                case _: pass
            
            # update the model with the message
            cmd = self.update(msg)
            
            if cmd is not None:
                await self._execute_cmd(cmd)
            
            # contanier used to draw elements from top to bottom
            view = Container() \
                .vertical() \
                .set(self.view())
                
            self._draw(view)
            
    def _draw(self, view: ElementBuilder):
        self._tb.clear()
        view.build().draw(self._tb)
        self._tb.print_buff()
            
    async def _execute_cmd(self, cmd: Cmd):
        async def run_cmd():
            try:
                if asyncio.iscoroutinefunction(cmd):
                    msg = await cmd()
                else:
                    loop = asyncio.get_event_loop()
                    msg = await loop.run_in_executor(None, cmd)
                
                if msg is not None:
                    await self.msg_queue.put(msg)
                    
            except Exception as e:
                print(e)
                
        asyncio.create_task(run_cmd())
        
    async def _input_task(self):
        try:
            inp = create_input()
            loop = asyncio.get_running_loop()

            with inp.raw_mode():
                while self._running:
                    keys = await loop.run_in_executor(None, inp.read_keys)
                    
                    for k in keys:
                        key_str = key_to_string(k)
                        await self.msg_queue.put(KeyPressMsg(key_str))
        except asyncio.CancelledError:
            pass
        
    def _hide_cursor(self):
        sys.stdout.write('\x1b[?25l') 
        sys.stdout.flush()
        
    def _show_cursor(self):
        sys.stdout.write('\x1b[?25h')
        sys.stdout.flush()