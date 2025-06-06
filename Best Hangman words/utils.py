"""Strings or values that may be used across multiple files."""

from enum import Enum
from typing import List, Tuple
from contextlib import contextmanager
import threading
import time

WORDLIST_PATH = "words_alpha.txt"
NON_ALPHA = r'''1234567890`~!@#$%^&*()_+-=[]{}\|;:'",.<>/?'''

def askUntilValid(prompt: str, valid: List[str]) -> str:
    """Repeats an input statement until a valid input is read.
    
    :param prompt: The message inside the input to ask the user
    :param valid: A list of valid strings that will be accepted.
    
    :returns: A valid string inputted by the user."""
    userResult = None
    while userResult not in valid:
        userResult = input(prompt)
    return userResult

def ceil(number: float) -> int:
    """Conditional for ceiling rounding.
    
    :returns: The rounded number."""
    if number - int(number) == 0:
        return int(number)
    else:
        return int(number) + 1

@contextmanager
def openDynamic(*args, **kwargs):
    """Fix for running scripts from the repo folder, crashing when run from the file directly.
    
    :param args: Positional arguments passed to the built-in open().
    :param kwargs: Keyword arguments passed to the built-in open().
    :yields: A file object like called by `open()`."""
    try:
        yield open(*args, **kwargs)
    except FileNotFoundError:
        oneOutArgs = (f"../{args[0]}",) + args[1:]
        yield open(*oneOutArgs, **kwargs)

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

    @classmethod
    def applyColour(cls, colour: "TerminalColours", string: str) -> None:
        """ Returns a message with the respective formatting applied.
        
        :param colour: The formatting to apply.
        :param string: The message to format.
        """
        return f'{colour.value}{string}{TerminalColours.END.value}'

    @classmethod
    def applyMulticolour(cls, colourStringPairs: List[Tuple["TerminalColours", str]]) -> None:
        """ Prints a message multiple formats applied.
        
        :param colourStringPairs: Tuple pairs of the formatting and message respectively.
        """
        finalString = ''
        for colour, word in colourStringPairs:
            finalString += f'{colour.value}{word}{TerminalColours.END.value}'
        return finalString

    @classmethod
    def applyAlternatingColour(cls, colours: List["TerminalColours"], string: str) -> None:
        """ Prints a message with cyclic alternating formats.
        
        :param colours: The colours/formats to apply, in order.
        :param string: The string to format.
        """
        finalString = ''
        for index, char in enumerate(list(string)):
            finalString += f"{colours[index % len(colours)].value}{char}{TerminalColours.END.value}"
        return finalString

    @classmethod
    def __testColours(cls):
        for x in [formatting for formatting in TerminalColours]:
            print(f"{x.value}{x}{TerminalColours.END.value}")

class BufferText:
    """Small class solely to hold a loading text function via multithreading."""
    runFlag = threading.Event()
    mainThread = None

    @classmethod
    @contextmanager
    def loadingText(cls, message: str ="Processing", endMessage:str=''):
        """Activates the loading text thread. To be used for in a `with` statement.
        Works best with no other stdout writing occuring while running.
        
        :param message: The message to print and append ellipses onto. Defaults to "Processing"
        :param endMessage: A message to print before exiting. By default, no message is printed."""
        cls.mainThread = threading.Thread(target=cls.__loadingAnimation, args=(message, endMessage))
        cls.mainThread.start()
        yield
        cls.runFlag.clear()
        cls.mainThread.join()

    @classmethod
    def __loadingAnimation(cls, message: str, endMsg: str = '') -> None:
        cls.runFlag.set()
        i = 0
        while cls.runFlag.is_set():
            dots = '.' * (i % 4)
            print(f"\r{message}{dots}   ", flush=True, end='')
            time.sleep(0.4)
            i += 1
        if endMsg == '':
            print(f"\r{' '*(len(message)+3)}\r", end='')
        else:
            print(f"\r{' '*(len(message)+3)}\r{endMsg}")
            

if __name__ == "__main__":
    print(TerminalColours.applyColour(TerminalColours.TEST, "test text"))
    print(TerminalColours.printMulticolour([(TerminalColours.REG_CYAN, "test "), (TerminalColours.REG_PINK, "message "), (TerminalColours.REG_YELLOW, "end")]))
    print(TerminalColours.printAlternatingColour([TerminalColours.REG_BLUE, TerminalColours.BKG_CYAN, TerminalColours.BLD_RED], "soliloquy"))
    TerminalColours.__testColours()
    with BufferText.loadingText():
        time.sleep(3)