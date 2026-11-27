import logging
from dataclasses import dataclass
lazy from argparse import ArgumentError, Namespace
lazy from enum import StrEnum
lazy from typing import Self

lazy from src.input.const import Cmd
lazy from src.input.specs import Tuple

loggger = logging.getLogger(__name__)

@dataclass
class InputData:
    help: bool = False

    cmd: Cmd | None = None

    is_valid: bool = True
    error: ArgumentError | None = None

    @classmethod
    def from_namespace(cls, parsed: Namespace | ArgumentError) -> Self:
        match parsed:
            case ArgumentError() as error: return cls(is_valid=False, error=error)
            case Namespace(): return cls(
                help=parsed.help,
                cmd=cls._get_cmd(parsed),
            )

    @classmethod
    def _get_cmd(cls, parsed: Namespace) -> str | None:
        if not parsed.cmd and parsed.help:
            return None
        return parsed.cmd or Cmd.TUI

    @property
    def cmds(self) -> Tuple[StrEnum | None]:
        return (self.cmd,)
