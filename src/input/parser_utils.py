from contextlib import contextmanager
from itertools import chain
lazy from argparse import ArgumentParser, _SubParsersAction
lazy from typing import Any, Generator


def iter_parsers(parser: ArgumentParser) -> Generator[ArgumentParser, Any]:
    yield parser
    for action in parser._actions:
        if isinstance(action, _SubParsersAction):
            for subparser in action.choices.values():
                yield from iter_parsers(subparser)


@contextmanager
def without_required(parser: ArgumentParser):
    parsers = list(iter_parsers(parser))

    requiring_required = [
        (requiring, requiring.required)
        for subparser in parsers
        for requiring in chain(
            subparser._actions,
            subparser._mutually_exclusive_groups
        )
    ]

    try:
        for requiring, _ in requiring_required:
            requiring.required = False
        yield parser
    finally:
        for requiring, required in requiring_required:
            requiring.required = required
