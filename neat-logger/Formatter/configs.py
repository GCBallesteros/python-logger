"""Potential log attributes and their names"""

from colorama import Fore

LOG_ATTRIBUTES_TO_NAME_AND_FORMAT_AND_COLOR_DICT = {
    "args": (None, None, Fore.WHITE),
    "created": (None, "f", Fore.YELLOW),
    "exc_info": (None, None, Fore.BLACK),
    "exc_text": (None, None, Fore.BLACK),
    "pathname": (None, "s", Fore.CYAN),
    "levelno": (None, "d", Fore.RED),
    "msecs": (None, "d", Fore.YELLOW),
    "thread": (None, "d", Fore.LIGHTBLUE_EX),
    "threadName": (None, "s", Fore.LIGHTBLUE_EX),
    "relativeCreated": (None, "d", Fore.YELLOW),
    "stack_info": (None, None, Fore.BLACK),
    "module": (None, "s", Fore.BLUE),
    "funcName": (None, "s", Fore.BLUE),
    "process": (None, "d", Fore.LIGHTGREEN_EX),
    "processName": (None, "s", Fore.LIGHTGREEN_EX),
    "asctime": ("timestamp", "s", Fore.YELLOW),
    "name": (None, "s", Fore.MAGENTA),
    "levelname": (None, "s", Fore.RED),
    "filename": (None, "s", Fore.CYAN),
    "lineno": (None, "d", Fore.CYAN),
}
# "msg" and "message" are excluded on purpose

DEFAULT_IGNORE_ATTRIBUTE_LIST = [
    "args",
    "created",
    "exc_info",
    "exc_text",
    "pathname",
    "levelno",
    "msecs",
    "threads",
    "threadName",
    "relativeCreated",
    "stack_info",
    "module",
    "funcName",
    "process",
    "processName",
]
