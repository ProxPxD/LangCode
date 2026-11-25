from dataclasses import dataclass
from typing import Self
lazy from argparse import Namespace

lazy from src.input.const import Cmd


@dataclass
class InputData:
    cmd: Cmd

    @classmethod
    def from_namespace(cls, namespace: Namespace) -> Self:
        return cls(
            cmd=namespace.cmd or Cmd.TUI,
        )
