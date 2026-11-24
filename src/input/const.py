from enum import auto

from src.utils.enum import IKebabCaseStrEnum


class Cmd(IKebabCaseStrEnum):
    TUI = auto()
    LOAD = auto()
