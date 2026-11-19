from dataclasses import dataclass
from enum import StrEnum, auto


class IKebabCaseStrEnum(StrEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values) -> str:
        return name.lower().replace('_', '-')

class IAppendClass(StrEnum):
    def __new__(cls, value: str):
        value = f'{value}-{cls.__name__.removesuffix("s")}'
        obj = str.__new__(cls, value)
        obj._value_ = value
        return obj


class WidgetClass(IKebabCaseStrEnum):
    COLUMN = auto()
    SHOW_COLUMN = auto()
    TITLE = auto()
    CONTENT = auto()


class WidgetID(IKebabCaseStrEnum):
    # Panels
    MAIN_COLUMN = auto()
    DISPLAY_COLUMN = auto()
    VIEW_COLUMN = auto()
    # Main Column Body
    REPL_PANE = auto()

class TuiText(StrEnum):
    # Main Column
    MAIN = 'Main'
    CONTEXT = 'Context'
