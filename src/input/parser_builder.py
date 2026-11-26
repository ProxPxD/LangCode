from argparse import ArgumentParser
import argparse
from collections.abc import Collection
from dataclasses import asdict, dataclass, field

import pydash as _

from . import specs


@dataclass(frozen=True)
class ParserTree:
    parser: ArgumentParser
    subparsers: dict[str, ParserTree] = field(default_factory=dict)


class ParserBuilder:
    _is_tui: bool | None = None

    @classmethod
    def build(cls, spec: specs.ParserSpec = specs.CLI, *, is_tui: bool) -> ParserTree:
        cls._is_tui = is_tui
        parser = ArgumentParser(
            prog='LangCode',
            description='Program for Coding Languages in',
            epilog='',
            exit_on_error=False,
        )
        parser_tree = cls._build_parser_tree(parser, spec)
        cls._is_tui = None
        return parser_tree

    @classmethod
    def _build_parser_tree(cls, parser: ArgumentParser, spec: specs.ParserSpec) -> ParserTree:
        for arg in spec.args:
            cls._add_argument(parser, arg)
        return ParserTree(
            parser=parser,
            subparsers=cls._build_subparsers_trees(parser, spec),
        )

    @classmethod
    def _add_argument(cls, parser: ArgumentParser, arg: specs.ArgSpec) -> None:
        kwargs = dict(arg.others)
        flags = _.to_list(arg.flags, split_strings=False)
        kwargs = cls._norm_kwargs(asdict(arg), drop='flags')
        parser.add_argument(*flags, **kwargs)

    @classmethod
    def _build_subparsers_trees(cls, parser: ArgumentParser, spec: specs.ParserSpec) -> frozendict[str, ParserTree]:
        if not spec.subs:
            return frozendict()
        subparsers_kwargs = cls._norm_kwargs(asdict(spec.subs_kwargs))
        subs = parser.add_subparsers(**subparsers_kwargs)
        subparsers: dict[str, ParserTree] = {}
        for sub_spec in spec.subs:
            if cls._is_tui and sub_spec.disable_for_tui:
                continue
            subparser_kwargs = cls._norm_kwargs(asdict(sub_spec), drop={'args', 'subs_kwargs', 'subs', 'disable_for_tui'})
            subparser: ArgumentParser = subs.add_parser(**subparser_kwargs)
            subparsers[sub_spec.name] = cls._build_parser_tree(subparser, sub_spec)
        return frozendict(**subparsers)

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
        start_parser.add_argument('arg', type=str, action='store')


        return parser
