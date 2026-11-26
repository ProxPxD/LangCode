from typing import Any, Protocol


class Executor(Protocol):
    def handle(self, input_data) -> Any: ...
