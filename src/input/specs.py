from dataclasses import dataclass, field
from typing import Any, Callable

from .const import Cmd

type Tuple[T] = tuple[T, ...]

UNSET = sentinel('UNSET')



@dataclass(frozen=True)
class ArgSpec:
    flags: Tuple[str] | str
    type:  Callable[[str], Any] | UNSET = UNSET
    dest: str | UNSET = UNSET
    action: str | UNSET = UNSET
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
    exit_on_error: bool = False
    others: frozendict[str, Any] = field(default_factory=frozendict)

    args: Tuple[ArgSpec] = ()
    subs_kwargs: SubsKwargsSpec | None = None
    subs: Tuple[ParserSpec] = ()

    disable_for_tui: bool = False
    add_help: bool = True

HELP = ArgSpec(('--help', '-h'), action='store_true', dest='help')

CLI = ParserSpec(
    args=(
        # ArgSpec(['--help', '-h'], action='store_true'),
    ),
    subs_kwargs=SubsKwargsSpec(dest='cmd', required=False),
    subs=(
        ParserSpec(
            name=Cmd.TUI,
            disable_for_tui=True,
        ),
        ParserSpec(
            name=Cmd.LOAD,
            args=(
                ArgSpec('file', type=str),
            ),
        ),
    ),
)

# c (start/run/tui)?

# c (query) <query>

# c <CMDS>:
# {query}
## ASK:       get conjugation hablar
## ADD/MOD:   set '1st-Person-Sg' in 'hablar' to 'hablo'
## ...
# {working}
## LOAD-INIT
## BIND
## EXPORT;
## ...

__all__ = [  # pyright: ignore[reportUnsupportedDunderAll]  # noqa: PLE0604
    'CLI',
    ArgSpec.__name__,
    SubsKwargsSpec.__name__,
    ParserSpec.__name__,
    UNSET.__name__
]
