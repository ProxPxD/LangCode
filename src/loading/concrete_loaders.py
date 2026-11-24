from enum import StrEnum, auto
lazy import json

lazy import pydash as _
lazy import yaml

from .abstract_loaders import DirLoader, FileLoader
lazy from .loader_protocol import Loader


class LoaderKind(StrEnum):
    ALL = auto()
    YAML = auto()
    JSON = auto()


FILE_LOADERS = {
    LoaderKind.YAML: FileLoader(lambda f: yaml.safe_load(f), ('.yaml', '.yml')),
    LoaderKind.JSON: FileLoader(lambda f: json.load(f), '.json'),
}


class LoaderProvider:
    @classmethod
    def get_for(cls, *kinds: LoaderKind) -> Loader:
        if LoaderKind.ALL in kinds:
            kinds = set(LoaderKind) - {LoaderKind.ALL}
        kinds = set(kinds)
        if None in (loaders := _.at(FILE_LOADERS, *kinds)):
            raise NotImplementedError(f'One of the following loader kinds has no implementation: {kinds}')
        return DirLoader(*loaders)
