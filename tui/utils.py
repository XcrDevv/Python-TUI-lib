from tui.colors import ANSI_REGEX
import string
from typing import List

nonascii_lower = 'áéíñóúý'
nonascii_upper = 'ÁÉÍÑÓÚÝ'
printable = string.printable + nonascii_lower + nonascii_upper

def wrap_text(text: str, max_width: int):
    splited_text: List[str] = []
    words = text.split()
    current_line = ''
    
    for word in words:
        if flat_len(current_line) + flat_len(word) + (1 if current_line else 0) > max_width:
            splited_text.append(current_line)
            current_line = word
        else:
            current_line += (' ' if current_line else '') + word
    
    if current_line:
        splited_text.append(current_line)
        
    return splited_text

def flat_len(string: str):
    return len(ANSI_REGEX.sub('', string))

def raw_str(string: str):
    return ANSI_REGEX.sub('', string)

from typing import Protocol

class SupportsStr(Protocol):
    def __str__(self) -> str: ...