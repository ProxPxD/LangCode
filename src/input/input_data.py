from enum import StrEnum
import logging
from dataclasses import dataclass
from typing import Self
lazy from argparse import Namespace

lazy from src.input.const import Cmd
lazy from src.input.specs import Tuple

loggger = logging.getLogger(__name__)

@dataclass
class InputData:
    help: bool
    cmd: Cmd

    @classmethod
    def from_namespace(cls, namespace: Namespace) -> Self:
        return cls(
            help=namespace.help,
            cmd=namespace.cmd or Cmd.TUI,
        )

    @property
    def cmds(self) -> Tuple[StrEnum]:
        return (self.cmd,)
