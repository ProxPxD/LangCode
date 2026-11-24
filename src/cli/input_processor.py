import logging
import shlex
import sys
from argparse import Namespace

import pydash as _
from pydash import chain as c

from src.cli.parser import ParserBuilder

logger = logging.getLogger(__name__)

class InputProcessor:
    def __init__(self, *, is_tui: bool) -> None:
        self.parser = ParserBuilder._build_playground(is_tui=is_tui)

    @classmethod
    def _norm_args(cls, args: list[str] | str | None) -> list[str]:
        args = _.default_to(args, sys.argv[1:])
        args = _.apply_if(args, shlex.split, _.is_string)
        args = _.flat_map(args, c().split('\xa0'))
        return args

    def _print_help_if_no_args(self, args: list[str]) -> None:
        if len(args) == 0:
            self.parser.print_help()
            sys.exit(0)

    def process(self, args: list[str] | str | None = None) -> Namespace:
        args: list[str] = self._norm_args(args)
        self._print_help_if_no_args(args)
        parsed = self.parser.parse_args(args)
        # parsed, remaining = self.parser.parse_known_args(args)
        # parsed.args += remaining
        logger.debug(f'Parsed: {parsed}')
        return parsed
