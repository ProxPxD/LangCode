from io import Reader
lazy from pathlib import Path
lazy from typing import Callable, Protocol

lazy from datatypes import DataType

type PathLike = str | Path
type LoadFunc = Callable[[Reader[str]], DataType]

class Loader(Protocol):
    def load(self, file: PathLike) -> DataType: ...
