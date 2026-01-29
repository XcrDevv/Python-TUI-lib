from prompt_toolkit.key_binding import KeyPress
from typing import List

KEY_ALIASES = {
    'c-h': 'backspace',
    'c-i': 'tab',
    'c-m': 'enter'
}

def key_to_string(k: KeyPress) -> str:
    parts: List[str] = []

    name = k.key

    if name in KEY_ALIASES:
        name = KEY_ALIASES[name]
        
    if name.startswith("c-"):
        parts.append("ctrl")
        name = name[2:]

    if name.startswith("a-"):
        parts.append("alt")
        name = name[2:]

    if name.startswith("s-"):
        parts.append("shift")
        name = name[2:]
        
    key = name
    parts.append(key)
    return "+".join(parts)