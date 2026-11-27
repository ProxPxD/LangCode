import argparse
import logging
import shlex
import sys
from contextlib import contextmanager
from typing import Any, Generator
lazy from argparse import ArgumentError, ArgumentParser, Namespace

import pydash as _
from pydash import chain as c
from textual.app import AppError

from src.input import parser_utils

from .parser_builder import ParserBuilder, ParserTree
lazy from .input_data import InputData

type ArgsLike = list[str] | str

logger = logging.getLogger(__name__)

class InputProcessor:
    def __init__(self, *, is_tui: bool) -> None:
        self.parser_tree: ParserTree = ParserBuilder.build(is_tui=is_tui)

    def process(self, args: ArgsLike | None = None) -> InputData:
        args: list[str] = self._norm_args(args);            logger.debug(f'Normalized args: {args}')
        parsed = self._parse(args);                         logger.debug(f'Parsed: {parsed}')
        input_data = InputData.from_namespace(parsed);      logger.debug(f'InputData: {input_data}')
        return input_data

    @classmethod
    def _norm_args(cls, args: ArgsLike | None) -> list[str]:
        args = _.default_to(args, sys.argv[1:])
        args = _.apply_if(args, shlex.split, _.is_string)
        args = _.flat_map(args, c().split('\xa0'))
        return args

    def _parse(self, args: list[str]) -> Namespace | ArgumentError:
        try:
            parsed = self.parser_tree.parser.parse_args(args)
        except ArgumentError:
            try:
                with parser_utils.without_required(self.parser_tree.parser) as parser:
                    parsed = parser.parse_args(args)
            except ArgumentError as ae:
                parsed = ae
        return parsed

