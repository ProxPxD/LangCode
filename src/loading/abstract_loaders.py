lazy from collections.abc import Callable, Sequence
lazy from pathlib import Path
lazy from typing import Protocol

import pydash as _
from _typeshed import SupportsRead

lazy from datatypes import DataType

type PathLike = str | Path
type LoadFunc = Callable[[SupportsRead[str]], DataType]

class Loader(Protocol):
    def load(self, file: PathLike) -> DataType: ...


class FileLoader:
    def __init__(self,
            load: LoadFunc,
            suffix_es: str | Sequence | None = None,
            is_loadable: Callable[[PathLike], bool] | None = None,
        ) -> None:
        self._load: LoadFunc = load
        self._suffixes: list[str] = _.to_list(suffix_es, split_strings=False) if suffix_es else []
        self._is_loadable = is_loadable or _.constant(True)

    def is_loadable(self, path: PathLike) -> bool:
        return Path(path).suffix in self._suffixes or self._is_loadable(path)

    def load(self, file: PathLike) -> DataType:
        result: DataType
        with Path(file).open() as f:
            result = self._load(f)
        return result


class DirLoader:
    def __init__(self, *file_loaders: FileLoader) -> None:
        self.file_loaders = file_loaders

    def _pick_file_loader(self, path: Path) -> FileLoader | None:
        return _.find(self.file_loaders, lambda loader: loader.is_loadable(path))  # pyright: ignore[reportCallIssue, reportAttributeAccessIssue]

    def load(self, file: PathLike) -> DataType:
        file = Path(file)
        if file.is_file():
            return self._load_file(file)
        if file.is_dir():
            return self._load_dir(file)
        raise ValueError(f'Unsupported filesystem entry: {file}')

    def _load_file(self, path: Path) -> DataType:
        if (loader := self._pick_file_loader(path)) is None:
            raise ValueError(f'Unsuported file extension: {path.suffix} [{path.name}]')
        return loader.load(path)

    def _load_dir(self, path: Path) -> dict[str, DataType]:
        return {
            subpath.stem: content
            for subpath in path.iterdir()
            if (content := self.load(subpath)) is not None
        }
