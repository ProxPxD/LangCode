import logging
import shlex
import sys
lazy from argparse import Namespace

import pydash as _
from pydash import chain as c

from .parser_builder import ParserBuilder
lazy from .input_data import InputData

type ArgsLike = list[str] | str

logger = logging.getLogger(__name__)

class InputProcessor:
    def __init__(self, *, is_tui: bool) -> None:
        self.parser = ParserBuilder.build(is_tui=is_tui)

    def process(self, args: ArgsLike | None = None) -> InputData:
        args: list[str] = self._norm_args(args); logger.debug(f'Normalized args: {args}')
        parsed = self._parse(args); logger.debug(f'Parsed: {parsed}')
        input_data = InputData.from_namespace(parsed); logger.debug(f'InputData: {input_data}')
        return input_data

    @classmethod
    def _norm_args(cls, args: ArgsLike | None) -> list[str]:
        args = _.default_to(args, sys.argv[1:])
        args = _.apply_if(args, shlex.split, _.is_string)
        args = _.flat_map(args, c().split('\xa0'))
        return args

    def _parse(self, args: list[str]) -> Namespace:
        parsed = self.parser.parse_args(args)
        # parsed, remaining = self.parser.parse_known_args(args)
        # parsed.args += remaining
        return parsed

