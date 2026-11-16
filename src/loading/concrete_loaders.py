from enum import StrEnum, auto
lazy import json

lazy import pydash as _
lazy import yaml

from .abstract_loaders import DirLoader, FileLoader, Loader


class LoaderKind(StrEnum):
    ALL = auto()
    YAML = auto()
    JSON = auto()


FILE_LOADERS = {
    LoaderKind.YAML: FileLoader(lambda f: yaml.safe_load(f), (".yaml", ".yml")),
    LoaderKind.JSON: FileLoader(lambda f: json.load(f), ".json"),
}


class LoaderProvider:
    @classmethod
    def get_for(cls, *kinds: LoaderKind) -> Loader:
        if LoaderKind.ALL in kinds:
            kinds = set(LoaderKind) - {LoaderKind.ALL}
        return DirLoader(*_.at(FILE_LOADERS, *kinds))
