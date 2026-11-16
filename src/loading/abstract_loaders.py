lazy from collections.abc import Callable, Sequence
lazy from pathlib import Path
lazy from typing import Any, Protocol, TextIO

import pydash as _

lazy from datatypes import DataType

type PathLike = str | Path

class Loader(Protocol):
    def load(self, file: PathLike) -> DataType: ...


class IPathAttr:
    def __init__(self, path: PathLike = None, *args: Any, **kwargs: Any) -> None:
        self.path: Path | None = Path(path) if path else None
        super().__init__(*args, **kwargs)


class FileLoader:
    def __init__(self,
            load: Callable[[PathLike | TextIO], dict],
            suffix_es: str | Sequence | None = None,
            is_loadable: Callable[[PathLike], bool] | None = None,
        ) -> None:
        self._load = load
        self._suffixes = _.to_list(suffix_es, split_strings=False) if suffix_es else []
        self._is_loadable = is_loadable or _.constant(True)

    def is_loadable(self, path: PathLike) -> bool:
        return Path(path).suffix in self._suffixes or self._is_loadable(path)

    def load(self, file: PathLike) -> DataType:
        try:
            result = self._load(file)
        except (OSError, ValueError, TypeError):
            with Path(file).open() as f:
                result = self._load(f)
        return result


class DirLoader(IPathAttr):
    def __init__(self, *file_loaders: FileLoader, **kwargs: Any) -> None:
        self.file_loaders = file_loaders
        super().__init__(**kwargs)

    def _pick_file_loader(self, path: Path) -> FileLoader | None:
        return _.find(self.file_loaders, lambda loader: loader.is_loadable(path))  # pyright: ignore[reportCallIssue, reportAttributeAccessIssue]

    def load(self, file: PathLike = None) -> DataType:
        file = Path(file) or self.path
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

