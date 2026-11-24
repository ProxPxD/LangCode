from dataclasses import dataclass, field
from typing import Any, Callable

type Tuple[T] = tuple[T, ...]

UNSET = sentinel('UNSET')


@dataclass(frozen=True)
class ArgSpec:
    flags: Tuple[str] | str
    type:  Callable[[str], Any] | UNSET = UNSET
    others: frozendict[str, Any] = field(default_factory=frozendict)

@dataclass(frozen=True)
class SubsKwargsSpec:
    dest: str
    required: bool | UNSET = UNSET
    others: frozendict[str, Any] = field(default_factory=frozendict)

@dataclass(frozen=True)
class ParserSpec:
    name: str | None = None
    help: str | UNSET = UNSET
    kwargs: frozendict[str, Any] = field(default_factory=frozendict)

    args: Tuple[ArgSpec] = ()
    subs_kwargs: SubsKwargsSpec = None
    subs: Tuple[ParserSpec] = ()

    disable_for_tui: bool = False


CLI = ParserSpec(
    args=(
    ),
    subs_kwargs=SubsKwargsSpec(dest='cmd', required=False),
    subs=(
        ParserSpec(
            name='tui',
            disable_for_tui=True,
        ),
        ParserSpec(
            name='load',
            args=(
                ArgSpec(
                    'file',
                    type=str,
                ),
            ),
        ),
    ),
)

__all__ = [  # pyright: ignore[reportUnsupportedDunderAll]  # noqa: PLE0604
    'CLI',
    ArgSpec.__name__,
    SubsKwargsSpec.__name__,
    ParserSpec.__name__,
]
