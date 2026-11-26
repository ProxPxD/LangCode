from typing import Protocol


class InputHandler(Protocol):
    def handle(self, data: str) -> str: ...

