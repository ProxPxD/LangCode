from collections.abc import Iterator

import pydash as _
from textual import events


class CmdHistory:
    def __init__(self) -> None:
        self.entries: list[str] = []
        self.index = 0

    def __iter__(self) -> Iterator:
        return iter(self.entries)

    def __len__(self) -> int:
        return len(self.entries)

    def get(self, index: int) -> str:
        return _.get(self.entries, index, '')

    def get_curr(self) -> str:
        return self.get(self.index)

    def add(self, cmd: str) -> None:
        self.entries.append(cmd)
        self.index = len(self.entries)

    def scroll(self, event: events.Key) -> bool:
        step: int = self._get_step_for_key(event)
        if 0 <= self.index + step <= len(self):
            self.index += step
            return True
        return False

    def _get_step_for_key(self, event: events.Key) -> int:
        match event.key:
            case 'up': return -1
            case 'down': return 1
            case _: raise ValueError(f'Unexpected key in cmd history handling: {event.key}')
