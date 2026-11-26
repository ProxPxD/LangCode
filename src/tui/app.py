
import logging

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Input
from textual_widgets import VerticalSplitter

from src.tui import css
from src.tui.executor_protocol import InputHandler

from .const import WidgetClass, WidgetID
from .display_panel import DisplayPanel
from .main_column import MainColumn, Terminal
from .view_panel import ViewPanel

logger = logging.getLogger(__name__)

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

        try:
            logger.debug(f'input submitted: {command}')
            output = self._input_handler.handle(command)
            logger.debug(f'output: {output}')
        except Exception:
            output = None



        if output:
            self.terminal.print(output)

        # TODO: remove
        logger.debug(f'Handling {command}')
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
        logger.debug(f'Finished handling: {command}')

