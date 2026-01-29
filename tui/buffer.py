import sys, os
import re
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class StyleRange:
    start: int
    end: int
    ansi_code: str

class TermBuffer:
    def __init__(self):
        self.num_columns = os.get_terminal_size().columns
        self.rows: list[str] = []
        self.style_rows: list[list[StyleRange]] = []
        self.saved_position = (0, 0)
        self.cursor = (0, 0)
    
    def _parse_styled_string(self, string: str) -> tuple[str, list[StyleRange]]:
        """Extract clean text and style ranges."""
        ansi_pattern = re.compile(r'\033\[[0-9;]*m')
        
        clean_chars: List[str] = []
        style_ranges: List[StyleRange] = []
        current_style = None
        style_start = None
        
        pos = 0
        visual_pos = 0
        
        while pos < len(string):
            match = ansi_pattern.match(string, pos)
            
            if match:
                code = match.group()
                
                if current_style and style_start is not None:
                    style_ranges.append(StyleRange(style_start, visual_pos, current_style))
                
                if '\033[0m' in code or code == '\033[m':
                    current_style = None
                    style_start = None
                else:
                    current_style = code
                    style_start = visual_pos
                
                pos = match.end()
            else:
                clean_chars.append(string[pos])
                visual_pos += 1
                pos += 1
        
        if current_style and style_start is not None:
            style_ranges.append(StyleRange(style_start, visual_pos, current_style))
        
        return ''.join(clean_chars), style_ranges
    
    def write_line(self, string: str):
        clean_text, styles = self._parse_styled_string(string)
        self.rows.append(clean_text)
        self.style_rows.append(styles)
    
    def write(self, string: str):
        x, y = self.cursor
        clean_text, new_styles = self._parse_styled_string(string)
        
        while len(self.rows) <= y:
            self.rows.append(' ' * self.num_columns)
            self.style_rows.append([])
        
        row = self.rows[y]
        end_x = x + len(clean_text)
        self.rows[y] = row[:x] + clean_text + row[end_x:]
        
        styles = self.style_rows[y]
        
        new_style_list: List[StyleRange] = []
        for style in styles:
            if style.end <= x or style.start >= end_x:
                # No intersection, maintain
                new_style_list.append(style)
            elif style.start < x and style.end > end_x:
                # The range completely surrounds the insertion, divide
                new_style_list.append(StyleRange(style.start, x, style.ansi_code))
                new_style_list.append(StyleRange(end_x, style.end, style.ansi_code))
            elif style.start < x < style.end:
                # Intersect on the right, trim
                new_style_list.append(StyleRange(style.start, x, style.ansi_code))
            elif style.start < end_x < style.end:
                # Intersect on the left, trim
                new_style_list.append(StyleRange(end_x, style.end, style.ansi_code))
        
        for style in new_styles:
            new_style_list.append(StyleRange(x + style.start, x + style.end, style.ansi_code))
        
        new_style_list.sort(key=lambda s: s.start)
        merged: List[StyleRange] = []
        for style in new_style_list:
            if merged and merged[-1].ansi_code == style.ansi_code and merged[-1].end == style.start:
                merged[-1] = StyleRange(merged[-1].start, style.end, style.ansi_code)
            else:
                merged.append(style)
        
        self.style_rows[y] = merged
        self.cursor = (end_x, y)
    
    def get_char(self, x: int | None = None, y: int | None = None) -> str:
        """Gets the visible character at a position."""
        if x is None or y is None:
            x, y = self.cursor
        
        if y >= len(self.rows) or x >= len(self.rows[y]):
            return ' '
        
        return self.rows[y][x]
    
    def get_style_at(self, x: int, y: int) -> Optional[str]:
        """Gets the active style at a position."""
        if y >= len(self.style_rows):
            return None
        
        for style in self.style_rows[y]:
            if style.start <= x < style.end:
                return style.ansi_code
        
        return None
    
    def add_style_to_char(self, x: int, y: int, new_style: str):
        """Adds a style to a single character, preserving the existing style."""
        current_style = self.get_style_at(x, y)
        
        combined = self._combine_styles(current_style, new_style)
        
        char = self.get_char(x, y)
        temp_cursor = self.cursor
        self.cursor = (x, y)
        self.write(f'{combined}{char}\033[0m')
        self.cursor = temp_cursor
    
    def _combine_styles(self, base: Optional[str], overlay: str) -> str:
        """Combine ANSI codes: extract parameters and merge them."""
        if not base:
            return overlay
        
        base_params = self._parse_ansi_params(base)
        overlay_params = self._parse_ansi_params(overlay)
        
        merged = {**base_params, **overlay_params}
        
        codes: List[str] = []
        if 'fg' in merged:
            codes.append(str(merged['fg']))
        if 'bg' in merged:
            codes.append(str(merged['bg']))
        for attr in ['bold', 'dim', 'italic', 'underline']:
            if merged.get(attr):
                codes.append(str({'bold': 1, 'dim': 2, 'italic': 3, 'underline': 4}[attr]))
        
        return f'\033[{";".join(codes)}m' if codes else ''
    
    def _parse_ansi_params(self, ansi: str) -> dict[str, int | bool]:
        """Extract parameters from ANSI code."""
        match = re.match(r'\033\[([0-9;]*)m', ansi)
        if not match:
            return {}
        
        codes = [int(c) for c in match.group(1).split(';') if c]
        params: dict[str, int | bool] = {}
        
        for code in codes:
            if 30 <= code <= 37 or 90 <= code <= 97:
                params['fg'] = code
            elif 40 <= code <= 47 or 100 <= code <= 107:
                params['bg'] = code
            elif code == 1:
                params['bold'] = True
            elif code == 2:
                params['dim'] = True
            elif code == 3:
                params['italic'] = True
            elif code == 4:
                params['underline'] = True
        
        return params
    
    def move_to(self, x: int, y: int):
        self.cursor = (x, y)
    
    def save_position(self):
        self.saved_position = self.cursor
    
    def restore_position(self):
        self.cursor = self.saved_position
    
    def next_line(self):
        self.cursor = (0, self.cursor[1] + 1)
    
    def prev_line(self):
        self.cursor = (0, max(0, self.cursor[1] - 1))
    
    def _reconstruct_row(self, row_idx: int) -> str:
        """Reconstruye una fila con estilos aplicados."""
        if row_idx >= len(self.rows):
            return ''
        
        text = self.rows[row_idx]
        styles = self.style_rows[row_idx] if row_idx < len(self.style_rows) else []
        
        if not styles:
            return text
        
        result: List[str] = []
        last_pos = 0
        
        for style in sorted(styles, key=lambda s: s.start):
            if style.start > last_pos:
                result.append(text[last_pos:style.start])
            
            result.append(f'{style.ansi_code}{text[style.start:style.end]}\033[0m')
            last_pos = style.end
        
        if last_pos < len(text):
            result.append(text[last_pos:])
        
        return ''.join(result)
    
    def print_buff(self):
        sys.stdout.write('\033[H')
        for i in range(len(self.rows)):
            row_with_styles = self._reconstruct_row(i)
            sys.stdout.write(row_with_styles + '\n')
        sys.stdout.flush()
    
    def clear(self):
        self.rows = [' ' * self.num_columns for _ in self.rows]
        self.style_rows = [[] for _ in self.style_rows]
        
    def clear_deep(self):
        self.clear()
        self.print_buff()
        self.rows = []
        self.style_rows = []