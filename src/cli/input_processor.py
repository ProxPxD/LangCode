import logging
import shlex
import sys
from argparse import Namespace

import pydash as _
from pydash import chain as c

from .parser_builder import ParserBuilder
from .specs import CLI

logger = logging.getLogger(__name__)

class InputProcessor:
    def __init__(self, *, is_tui: bool) -> None:
        self.parser = ParserBuilder.build(CLI, is_tui=is_tui)

    @classmethod
    def _norm_args(cls, args: list[str] | str | None) -> list[str]:
        args = _.default_to(args, sys.argv[1:])
        args = _.apply_if(args, shlex.split, _.is_string)
        args = _.flat_map(args, c().split('\xa0'))
        return args

    def process(self, args: list[str] | str | None = None) -> Namespace:
        args: list[str] = self._norm_args(args)
        logger.debug(f'Normalized args: {args}')
        parsed = self.parser.parse_args(args)
        # parsed, remaining = self.parser.parse_known_args(args)
        # parsed.args += remaining
        logger.debug(f'Parsed: {parsed}')
        return parsed
