from enum import StrEnum, auto
lazy import json

lazy import yaml

from src.loading.abstract_loaders import DirLoader, FileLoader, Loader


class LoaderKind(StrEnum):
    ALL = auto()
    YAML = auto()
    JSON = auto()


FILE_LOADERS = {
    LoaderKind.YAML: FileLoader(lambda f: yaml.safe_load(f), ('.yaml', '.yml')),
    LoaderKind.JSON: FileLoader(lambda f: json.load(f), '.json'),
}

class DataLoaderProvider:
    @classmethod
    def get(cls, kind: LoaderKind) -> Loader:
        match kind:
            case LoaderKind.ALL: return DirLoader(*tuple(FILE_LOADERS.values()))
            case _: return FILE_LOADERS[kind]
