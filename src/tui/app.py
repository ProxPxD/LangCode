
from textual import events
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Input, RichLog, Static
from textual_widgets import VerticalSplitter

from src.tui.const import WidgetClass, WidgetID
from src.tui.display_panel import DisplayPanel
from src.tui.main_column import MainColumn
from src.tui.view_panel import ViewPanel

from .tmp_css import CSS


class TerminalTUI(App):
    CSS = f'''
    {VerticalSplitter.__name__} {{
        height: 100%;
        width: 1;
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
    '''

    BINDINGS = (
        ("ctrl+c", "quit", "Quit"),
    )

    def __init__(self) -> None:
        super().__init__()
        self.history: list[str] = []
        self.history_index = 0

    def compose(self) -> ComposeResult:
        with Horizontal(id="main"):
            yield ViewPanel()
            yield VerticalSplitter()
            yield MainColumn()
            yield VerticalSplitter()
            yield DisplayPanel()

    # def on_mount(self) -> None:
    #     self.query_one("#view-log", RichLog).write(
    #         "[green]$ system monitor[/]\n"
    #         "CPU: 12%\n"
    #         "RAM: 4.2 GB\n"
    #         "Processes: 128\n"
    #         "Network: connected"
    #     )

    #     self.query_one("#display-log", RichLog).write(
    #         "[green]$ application logs[/]\n"
    #         "[dim]10:32:01[/] Application started\n"
    #         "[dim]10:32:02[/] Configuration loaded\n"
    #         "[yellow]10:32:05[/] Waiting for input..."
    #     )

    #     self.query_one("#repl-log", RichLog).write(
    #         "[bold green]Interactive REPL[/]\n"
    #         "Type 'help' to see available commands."
    #     )

    #     self.query_one("#command", Input).focus()

    # def on_input_submitted(self, event: Input.Submitted) -> None:
    #     command = event.value.strip()
    #     event.input.value = ""

    #     if not command:
    #         return

    #     self.history.append(command)
    #     self.history_index = len(self.history)

    #     log = self.query_one("#repl-log", RichLog)
    #     log.write(f"[bold cyan]>>> {command}[/]")

    #     if command == "help":
    #         log.write("Available commands: help, status, clear, exit")

    #     elif command == "status":
    #         log.write("Application is running.")

    #     elif command == "clear":
    #         log.clear()

    #     elif command == "exit":
    #         self.exit()

    #     else:
    #         log.write(f"[yellow]Unknown command:[/] {command}")

    # def on_key(self, event: events.Key) -> None:
    #     if self.focused is not self.query_one("#command", Input):
    #         return

    #     if event.key == "up":
    #         if self.history and self.history_index > 0:
    #             self.history_index -= 1
    #             self._restore_command()
    #             event.prevent_default()
    #             event.stop()

    #     elif event.key == "down":
    #         if self.history_index < len(self.history):
    #             self.history_index += 1
    #             self._restore_command()
    #             event.prevent_default()
    #             event.stop()

    # def _restore_command(self) -> None:
    #     command_input = self.query_one("#command", Input)

    #     if self.history_index < len(self.history):
    #         command_input.value = self.history[self.history_index]
    #     else:
    #         command_input.value = ""

    #     command_input.cursor_position = len(command_input.value)
