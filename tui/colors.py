import re

ANSI_REGEX = re.compile(r'\x1B\[[0-9;]*[mK]')

ANSI_RESET = '\033[0m'

ANSI_COLORS = {
    'black': '\033[30m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'gray': '\033[90m',
    'light_gray': '\033[37m',
    'dark_gray': '\033[90m',
}

ANSI_BG = {
    'black': '\033[48;5;0m',
    'red': '\033[48;5;1m',
    'green': '\033[48;5;2m',
    'yellow': '\033[48;5;3m',
    'blue': '\033[48;5;4m',
    'magenta': '\033[48;5;5m',
    'cyan': '\033[48;5;6m',
    'white': '\033[48;5;7m',
}

def background(text: str, color: str):
    return f'{ANSI_BG[color]}{text}{ANSI_RESET}'

def colored(text: str, color: str):
    return f'{ANSI_COLORS[color]}{text}{ANSI_RESET}'

def black(text: str):
    return f'\033[30m{text}{ANSI_RESET}'

def red(text: str):
    return f'\033[31m{text}{ANSI_RESET}'

def green(text: str):
    return f'\033[32m{text}{ANSI_RESET}'

def yellow(text: str):
    return f'\033[33m{text}{ANSI_RESET}'

def blue(text: str):
    return f'\033[34m{text}{ANSI_RESET}'

def magenta(text: str):
    return f'\033[35m{text}{ANSI_RESET}'

def cyan(text: str):
    return f'\033[36m{text}{ANSI_RESET}'

def white(text: str):
    return f'\033[37m{text}{ANSI_RESET}'

def gray(text: str):
    return f'\033[90m{text}{ANSI_RESET}'

def bold(text: str):
    return f'\033[1m{text}\033[0m'

def print_format_table():
    """
    prints table of formatted text format options 
    """
    for style in range(8):
        for fg in range(30,38):
            s1 = ''
            for bg in range(40,48):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
            print(s1)
        print('\n')