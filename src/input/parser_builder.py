from argparse import ArgumentParser
from collections.abc import Collection
from dataclasses import asdict

import pydash as _

from . import specs


class ParserBuilder:
    _is_tui: bool | None = None

    @classmethod
    def build(cls, spec: specs.ParserSpec = specs.CLI, *, is_tui: bool) -> ArgumentParser:
        cls._is_tui = is_tui
        parser = ArgumentParser(
            prog='LangCode',
            description='Program for Coding Languages in',
            epilog='',
        )
        cls._build_parser(parser, spec)
        cls._is_tui = None
        return parser

    @classmethod
    def _build_parser(cls, parser: ArgumentParser, spec: specs.ParserSpec) -> None:
        for arg in spec.args:
            cls._build_argument(parser, arg)
        if spec.subs:
            cls._build_subparsers(parser, spec)

    @classmethod
    def _build_argument(cls, parser: ArgumentParser, arg: specs.ArgSpec) -> None:
        kwargs = dict(arg.others)
        flags = _.to_list(arg.flags, split_strings=False)
        kwargs = cls._norm_kwargs(asdict(arg), drop='flags')
        parser.add_argument(*flags, **kwargs)

    @classmethod
    def _build_subparsers(cls, parser: ArgumentParser, spec: specs.ParserSpec) -> None:
        subparsers_kwargs = cls._norm_kwargs(asdict(spec.subs_kwargs))
        subs = parser.add_subparsers(**subparsers_kwargs)
        for sub_spec in spec.subs:
            if cls._is_tui and sub_spec.disable_for_tui:
                continue
            cls._norm_kwargs(asdict(sub_spec), drop={'args', 'subs_kwargs', 'subs', 'disable_for_tui'})
            subparser = subs.add_parser(sub_spec.name)
            cls._build_parser(subparser, sub_spec)

    @classmethod
    def _norm_kwargs(cls, kwargs: dict, *, drop: str | Collection[str] | None = None) -> dict:
        drop = _.to_list(drop or [], split_strings=False)
        rest = {key: val for key, val in kwargs.items() if key not in {'others', *drop} and val is not specs.UNSET}
        return {**rest, **kwargs.get('others', {})}

    # ----

    @classmethod
    def _build_playground(cls, *, is_tui: bool) -> ArgumentParser:
        parser = ArgumentParser(prog='TestCode', description='Checking arguments')

        sub = parser.add_subparsers(dest='cmd', required=False)
        start_parser = sub.add_parser('start', help='Enter main loop')
        start_parser.add_argument('arg', type=str)

        return parser
