from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import RichLog, Static

from src.tui.const import WidgetClass, WidgetID


class DisplayPanel(Vertical):
    def __init__(self) -> None:
        super().__init__(id=WidgetID.DISPLAY_COLUMN, classes=f'{WidgetClass.COLUMN} {WidgetClass.SHOW_COLUMN}')

    def compose(self) -> ComposeResult:
        yield Static("[bold cyan]Display[/]\n", classes=WidgetClass.TITLE)
        yield RichLog(id="display-log", wrap=True, markup=True)

