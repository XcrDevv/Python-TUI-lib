from tui.elements.cursor.model import CursorModel
from tui.messages import Msg, KeyPressMsg
from tui.commands import Cmd
from tui.utils import printable
from tui.app import gen_id
from typing import List, Literal

class TextInputModel:
    def __init__(self):
        self._id = gen_id()
        self._focused = False
        self._blink_gen = 0
        self._current_suggestion = ''
        self.cursor = CursorModel()
        self.value = ''
        self.suggestions: List[str]  = []
        
    def set_value(self, value: str):
        self.value = value
        self.cursor.set_to(len(value))
        
    def update_suggestion(self):
        self._current_suggestion = ''
        for suggestion in self.suggestions:
            if suggestion.startswith(self.value) and self.value:
                self._current_suggestion = suggestion
                
    def jump_word(self, dir: Literal['left', 'right']) -> int:
        rest = self.value[:self.cursor.pos[1] - 1] if dir == 'left' else self.value[self.cursor.pos[1] + 1:]
        
        offset = 1
        
        for c in reversed(rest) if dir == 'left' else rest:
            if c == ' ':
                break
            offset += 1
        else:
            len(rest)
            
        return offset * -1 if dir == 'left' else offset
             
    def update(self, msg: Msg) -> Cmd | None:
        if not isinstance(msg, KeyPressMsg) or not self.focused():
            return self.cursor.update(msg)
        
        match msg.key:
            case 'backspace' | 'delete' as key:
                if self.cursor.has_selection():
                    start = min(self.cursor.pos)
                    end = max(self.cursor.pos)
                    self.value = self.value[:start] + self.value[end:]
                    self.cursor.set_to(start)
                if key == 'backspace':
                    if not self.cursor.has_selection() and len(self.value) > 0 and self.cursor.pos[0] > 0:
                        self.value = self.value[:self.cursor.pos[0] - 1] + self.value[self.cursor.pos[1]:]
                        self.cursor.offset(-1)
                else:
                    if not self.cursor.has_selection():
                        self.value = self.value[:self.cursor.pos[0]] + self.value[self.cursor.pos[1] + 1:]
                self.update_suggestion()
                self.cursor.rst_blink()
            case 'left':
                if self.cursor.has_selection():
                    self.cursor.set_to(min(self.cursor.pos))
                elif self.cursor.pos[0] > 0:
                        self.cursor.offset(-1)
                        self.cursor.rst_blink()
            case 'right':
                if self.cursor.has_selection():
                    self.cursor.set_to(max(self.cursor.pos))
                elif self.cursor.pos[0] < len(self.value):
                    self.cursor.offset(1)
                    self.cursor.rst_blink()
            case key if key in printable and key not in '\t\n\r':
                start = min(self.cursor.pos)
                end = max(self.cursor.pos)
                self.value = self.value[:start] + key + self.value[end:]
                if self.cursor.has_selection():
                    self.cursor.set_to(start)
                self.cursor.offset(1)
                self.cursor.rst_blink()
                self.update_suggestion()
            case 'home':
                self.cursor.set_to(0)
            case 'end':
                self.cursor.set_to(len(self.value))
            case 'ctrl+a':
                self.cursor.set_anchor(0)
                self.cursor.set_displacement(len(self.value))
            case 'ctrl+left':
                if self.cursor.pos[1] > 0:
                    self.cursor.offset(self.jump_word('left'))
            case 'ctrl+right':
                if self.cursor.pos[1] < len(self.value):
                    self.cursor.offset(self.jump_word('right'))
            case 'shift+left':
                if self.cursor.pos[1] > 0:
                    self.cursor.offset_displacement(-1)
            case 'shift+right':
                if self.cursor.pos[1] < len(self.value):
                    self.cursor.offset_displacement(+1)
            case 'ctrl+shift+left':
                if self.cursor.pos[1] > 0:
                    self.cursor.offset_displacement(self.jump_word('left'))
            case 'ctrl+shift+right':
                if self.cursor.pos[1] < len(self.value):
                    self.cursor.offset_displacement(self.jump_word('right'))
            case 'ctrl+shift+home':
                self.cursor.set_displacement(0)
            case 'ctrl+shift+end':
                self.cursor.set_displacement(len(self.value))
            case 'tab':
                if self._current_suggestion:
                    self.value = self._current_suggestion
                    self.cursor.set_to(len(self.value))
                    self._current_suggestion = ''
                    
        return self.cursor.update(msg)
    
    @property
    def current_suggestion(self):
        return self._current_suggestion
    
    def focused(self) -> bool:
        return self._focused
    
    def focus(self) -> Msg:
        self._focused = True
        return self.cursor.focus()
        
    def blur(self):
        self._focused = False
        return self.cursor.blur()