from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import RichLog, Static

from src.tui.const import WidgetClass, WidgetID


class ViewPanel(Vertical):
    def __init__(self) -> None:
        super().__init__(id=WidgetID.VIEW_COLUMN, classes=f'{WidgetClass.COLUMN} {WidgetClass.SHOW_COLUMN}')

    def compose(self) -> ComposeResult:
        yield Static("[bold cyan]View[/]\n", classes=WidgetClass.TITLE)
        yield RichLog(id="view-log", wrap=True, markup=True)

