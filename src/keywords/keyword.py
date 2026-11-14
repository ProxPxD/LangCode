from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True, init=False)
class Keyword:
    main: str
    alts: frozenset[str] = field(default_factory=frozenset)

    def __init__(self, main: str, *alts: str):
        self.__setattr__('main',  main)
        self.__setattr__('alts',  frozenset(alts))

    @property
    def forms(self) -> frozenset[str]:
        return frozenset({self.main, *self.alts})

    def __contains__(self, val: Any) -> bool:
        match val:
            case str(): return val in self.forms
            case _: return False
