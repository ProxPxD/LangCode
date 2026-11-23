import logging
import shlex
import sys
from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace

import pydash as _
from pydash import chain as c

logger = logging.getLogger(__name__)


class CLI(ABC):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def parse(self, args: list[str] | str = None) -> Namespace:
        args = _.apply_if(args, shlex.split, _.is_string) or sys.argv[1:]
        args = [*arg.split('\xa0') for arg in args]
        if len(args) == 0:
            self.parser.print_help()
            sys.exit(0)
        parsed = self.parser.parse_args(args)
        # parsed, remaining = self.parser.parse_known_args(args)
        # parsed.args += remaining

        logger.debug(f'Parsed: {parsed}')
        return parsed

    @property
    def parser(self) -> ArgumentParser:
        ...
