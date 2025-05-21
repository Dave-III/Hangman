"""Strings or values that may be used across multiple files."""

from enum import Enum

WORDLIST_PATH = "words_alpha.txt"
NON_ALPHA = r'''1234567890`~!@#$%^&*()_+-=[]{}\|;:'",.<>/?'''

class TerminalColours(Enum):
    PINK = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

    @staticmethod
    def printColor(colour: "TerminalColours", string):
        print(f'{colour.value}{string}{TerminalColours.END.value}')

    # TODO more colour print variations

if __name__ == "__main__":
    TerminalColours.printColor(TerminalColours.PINK, "test text")
    TerminalColours.printColor(TerminalColours.RED, "test text")