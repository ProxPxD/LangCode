from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import RichLog, Static

from .const import TextFormatting, WidgetClass, WidgetID


class DisplayPanel(Vertical):
    def __init__(self) -> None:
        super().__init__(id=WidgetID.DISPLAY_COLUMN, classes=f'{WidgetClass.COLUMN} {WidgetClass.SHOW_COLUMN}')

    def compose(self) -> ComposeResult:
        yield Static(f"[{TextFormatting.TITLE}]Display[/]\n", classes=WidgetClass.TITLE)
        yield RichLog(id="display-log", wrap=True, markup=True, classes=WidgetClass.SHOW_CONTENT)

