from enum import StrEnum, auto

from src.utils.enum import IKebabCaseStrEnum


class WidgetClass(IKebabCaseStrEnum):
    COLUMN = auto()
    SHOW_COLUMN = auto()
    SHOW_CONTENT = auto()
    TITLE = auto()
    CONTENT = auto()
    SPLITTER = auto()


class WidgetID(IKebabCaseStrEnum):
    # Panels
    MAIN_COLUMN = auto()
    DISPLAY_COLUMN = auto()
    VIEW_COLUMN = auto()
    # Main Column
    CONSOLE_PANE = auto()
    CONTEXT_PANE = auto()
    ## Console Pane
    TERMINAL = auto()
    CMD_LOG = auto()
    CMD_PROMPT = auto()
    CMD_INPUT = auto()

class TuiText(StrEnum):
    # Main Column
    MAIN = 'Main'
    CONTEXT = 'Context'
    PROMPT = '> '


class TextFormatting(StrEnum):
    TITLE = 'bold green'
