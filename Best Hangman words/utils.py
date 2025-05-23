"""Strings or values that may be used across multiple files."""

from enum import Enum
from typing import List, Tuple
import time

WORDLIST_PATH = "words_alpha.txt"
NON_ALPHA = r'''1234567890`~!@#$%^&*()_+-=[]{}\|;:'",.<>/?'''

class TerminalColours(Enum):
    """Class for holding common colours and formats for CLI usage."""
    END = '\033[0m'

    # There doesn't appear to be a visual distinction between standard and high-intensity colours
    # on windows powershell.
    # Regular Formatting
    REG_GREY = '\033[0;90m'
    REG_RED = '\033[0;91m'
    REG_GREEN = '\033[0;92m'
    REG_YELLOW = '\033[0;93m'
    REG_BLUE = '\033[0;94m'
    REG_PINK = '\033[0;95m'
    REG_CYAN = '\033[0;96m'
    REG_WHITE = '\033[0;97m'
    
    # Bold
    BLD_GREY = '\033[1;30m'
    BLD_RED = '\033[1;31m'
    BLD_GREEN = '\033[1;32m'
    BLD_YELLOW = '\033[1;33m'
    BLD_BLUE = '\033[1;34m'
    BLD_PINK = '\033[1;35m'
    BLD_CYAN = '\033[1;36m'
    BLD_WHITE = '\033[1;37m'

    # Underlined
    UDL_GREY = '\033[4;30m'
    UDL_RED = '\033[4;31m'
    UDL_GREEN = '\033[4;32m'
    UDL_YELLOW = '\033[4;33m'
    UDL_BLUE = '\033[4;34m'
    UDL_PINK = '\033[4;35m'
    UDL_CYAN = '\033[4;36m'
    UDL_WHITE = '\033[4;37m'

    # Background
    BKG_GREY = '\033[0;100m'
    BKG_RED = '\033[0;101m'
    BKG_GREEN = '\033[0;102m'
    BKG_YELLOW = '\033[0;103m'
    BKG_BLUE = '\033[0;104m'
    BKG_PINK = '\033[0;105m'
    BKG_CYAN = '\033[0;106m'
    BKG_WHITE = '\033[0;107m'
    
    TEST = '\033[38;5;52m'

    @staticmethod
    def printColour(colour: "TerminalColours", string: str) -> None:
        """ Prints a message with the respective formatting applied.
        
        :param colour: The formatting to apply.
        :param string: The message to format.
        """
        print(f'{colour.value}{string}{TerminalColours.END.value}')

    @staticmethod
    def printMulticolour(colourStringPairs: List[Tuple["TerminalColours", str]]) -> None:
        """ Prints a message multiple formats applied.
        
        :param colourStringPairs: Tuple pairs of the formatting and message respectively.
        """
        finalString = ''
        for colour, word in colourStringPairs:
            finalString += f'{colour.value}{word}{TerminalColours.END.value}'
        print(finalString)

    @staticmethod
    def printAlternatingColour(colours: List["TerminalColours"], string: str) -> None:
        """ Prints a message with cyclic alternating formats.
        
        :param colours: The colours/formats to apply, in order.
        :param string: The string to format.
        """
        finalString = ''
        for index, char in enumerate(list(string)):
            finalString += f"{colours[index % len(colours)].value}{char}{TerminalColours.END.value}"
        print(finalString)

    @staticmethod
    def _testColours():
        for x in [formatting for formatting in TerminalColours]:
            print(f"{x.value}{x}{TerminalColours.END.value}")

class BufferText:
    def __init__(self):
        pass

    def loading_animation(message="Processing"):
        i = 0
        while True:
            dots = '.' * (i % 4)
            print(f"\rTest{dots}   ", flush=True, end='')
            time.sleep(0.5)
            i += 1

if __name__ == "__main__":
    TerminalColours.printColour(TerminalColours.TEST, "test text")
    TerminalColours.printMulticolour([(TerminalColours.REG_CYAN, "test "), (TerminalColours.REG_PINK, "message "), (TerminalColours.REG_YELLOW, "end")])
    TerminalColours.printAlternatingColour([TerminalColours.REG_BLUE, TerminalColours.BKG_CYAN, TerminalColours.BLD_RED], "soliloquy")
    TerminalColours._testColours()
    # q = BufferText()
    # q.loading_animation()