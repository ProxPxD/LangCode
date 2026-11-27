import logging
from dataclasses import dataclass
from enum import StrEnum
from typing import Self
lazy from argparse import Namespace

lazy from src.input.const import Cmd
lazy from src.input.specs import Tuple

loggger = logging.getLogger(__name__)

@dataclass
class InputData:
    help: bool
    cmd: Cmd | None

    @classmethod
    def from_namespace(cls, parsed: Namespace) -> Self:
        return cls(
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
