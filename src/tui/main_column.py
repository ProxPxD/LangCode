from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Input, RichLog, Static

from src.tui.const import TuiText, WidgetClass, WidgetID


class MainColumn(Vertical):
    def __init__(self) -> None:
        super().__init__(
            id=WidgetID.MAIN_COLUMN,
            classes=WidgetClass.COLUMN,
        )

    def compose(self) -> ComposeResult:
        with Vertical(id='repl'):
            yield Static(f'[bold green]{TuiText.MAIN}[/]', classes=WidgetClass.TITLE)
            yield RichLog(id=WidgetID.REPL_PANE, wrap=True, markup=True)
            yield Input(
                placeholder="Enter command... (WidgetClass.panels.MAIN)",
                id="command",
            )
        yield Static(
            f'[bold yellow]{TuiText.CONTEXT}[/]\n'
            'Ready.\n'
            '↑ / ↓ Navigate command history.',
            id='bottom',
        )
