
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Input, RichLog
from textual_widgets import HorizontalSplitter, VerticalSplitter

from src.tui import css
from src.tui.executor_protocol import InputHandler

from .const import TuiText, WidgetClass, WidgetID
from .display_panel import DisplayPanel
from .main_column import MainColumn, Terminal
from .view_panel import ViewPanel


class Tui(App):
    CSS = css.TUI_CSS

    BINDINGS = [  # noqa: RUF012
        ("ctrl+c", "quit", "Quit"),
    ]

    def __init__(self, input_handler: InputHandler) -> None:
        super().__init__()
        self._input_handler = input_handler

    def compose(self) -> ComposeResult:
        with Horizontal(id="main"):
            yield ViewPanel()
            yield VerticalSplitter(classes=WidgetClass.SPLITTER)
            yield MainColumn()
            yield VerticalSplitter(classes=WidgetClass.SPLITTER)
            yield DisplayPanel()

    def on_mount(self) -> None:
        self.terminal: Terminal = self.query_one(f'#{WidgetID.TERMINAL}', Terminal)
        self.query_one(f'#{WidgetID.CMD_INPUT}', Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        command = event.value.strip()
        event.input.value = ""

        if not command:
            return

        output = self._input_handler.handle(command)
        self.terminal.print(output)

        if command == "help":
            self.terminal.print("Available commands: help, status, clear, exit")

        elif command == "status":
            self.terminal.print("Application is running.")
        elif command == "clear":
            self.terminal.clear()
        elif command == "exit":
            self.exit()
        else:
            self.terminal.print(f"[yellow]Unknown command:[/] {command}")

