
from textual import events
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Input, RichLog, Static
from textual_widgets import VerticalSplitter

from src.tui.const import TuiText, WidgetClass, WidgetID
from src.tui.display_panel import DisplayPanel
from src.tui.main_column import MainColumn, Terminal
from src.tui.view_panel import ViewPanel

from .tmp_css import CSS


class TerminalTUI(App):
    CSS = f'''
    {VerticalSplitter.__name__} {{
        height: 100%;
        width: 1;
    }}

    {VerticalSplitter.__name__}:hover,
    {VerticalSplitter.__name__}.dragging {{
        background: darkgreen;
    }}

    .{WidgetClass.TITLE} {{
        height: 1;
    }}

    .{WidgetClass.COLUMN} {{
        height: 1fr;
    }}

    #{WidgetID.MAIN_COLUMN} {{
        width: 2fr;
    }}

    .{WidgetClass.SHOW_COLUMN} {{
        width: 1fr;
    }}

    {RichLog.__name__}:focus, {Input.__name__}:focus {{
        background-tint: transparent;
    }}

    .{WidgetClass.SHOW_CONTENT} {{
        background: transparent;
    }}

    {RichLog.__name__} {{
        scrollbar-size-vertical: 1;
        scrollbar-size-horizontal: 0;

        scrollbar-color: $text-muted 25%;
        scrollbar-color-hover: $text-muted 60%;

        scrollbar-background: transparent;
        scrollbar-background-hover: transparent;
    }}
    '''

    BINDINGS = (
        ("ctrl+c", "quit", "Quit"),
    )

    def __init__(self) -> None:
        super().__init__()

    def compose(self) -> ComposeResult:
        with Horizontal(id="main"):
            yield ViewPanel()
            yield VerticalSplitter()
            yield MainColumn()
            yield VerticalSplitter()
            yield DisplayPanel()

    def on_mount(self) -> None:
        self.terminal: Terminal = self.query_one(f'#{WidgetID.TERMINAL}', Terminal)
        self.query_one(f'#{WidgetID.CMD_INPUT}', Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        command = event.value.strip()
        event.input.value = ""

        if not command:
            return

        log = self.query_one(f'#{WidgetID.CMD_LOG}', RichLog)
        log.write(f'{TuiText.PROMPT} {command}')

        if command == "help":
            log.write("Available commands: help, status, clear, exit")

        elif command == "status":
            log.write("Application is running.")

        elif command == "clear":
            log.clear()

        elif command == "exit":
            self.exit()

        else:
            log.write(f"[yellow]Unknown command:[/] {command}")

