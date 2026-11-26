from typing import Text

from textual import events
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Input, RichLog, Static
from textual_widgets import HorizontalSplitter

from .const import TextFormatting, TuiText, WidgetClass, WidgetID
from .history import CmdHistory


class CmdLine(Horizontal):
    DEFAULT_CSS = f'''
        #{WidgetID.CMD_PROMPT} {{
            height: 1fr;
            width: {len(TuiText.PROMPT)};
        }}

        #{WidgetID.CMD_INPUT} {{
            height: 1fr;
            width: 1fr;
        }}
    '''

    def compose(self) -> ComposeResult:
        yield Static(TuiText.PROMPT, id=WidgetID.CMD_PROMPT)
        yield Input(id=WidgetID.CMD_INPUT, compact=True)


class Terminal(Vertical):
    DEFAULT_CSS = f'''
        #{WidgetID.CMD_LOG} {{
            border: none;
            background: $surface;
            padding: 0;
            height: 1fr;
        }}

        {CmdLine.__name__} {{
            border: none;
            background: $surface;
            padding: 0;
            height: 1;
            padding: 0;
            margin: 0;
        }}
    '''

    def __init__(self) -> None:
        super().__init__(id=WidgetID.TERMINAL)
        self.cmd_history = CmdHistory()
        self.log_entries = []

    def compose(self) -> ComposeResult:
        yield RichLog(wrap=True, markup=True, id=WidgetID.CMD_LOG)
        yield CmdLine()

    def _on_mount(self, event: events.Mount) -> None:
        self.cmd_log = self.query_one(f'#{WidgetID.CMD_LOG}', RichLog)
        self.cmd_input = self.query_one(f'#{WidgetID.CMD_INPUT}', Input)

    def on_resize(self, event: events.Resize) -> None:
        self.cmd_log.clear()
        for entry in self.log_entries:
            self.cmd_log.write(entry)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        command = event.value.strip()
        self.cmd_history.add(command)
        self.print(f'{TuiText.PROMPT} {command}')

    def print(self, text: str) -> None:
        self.log_entries.append(text)
        self.cmd_log.write(text)

    def clear(self) -> None:
        self.cmd_history.clear()
        self.log_entries.clear()
        self.cmd_log.clear()
        self._restore_command()

    def _on_click(self, event: events.Click) -> None:
        self.cmd_input.focus()

    def on_key(self, event: events.Key) -> None:
        if event.key in {'up', 'down'}:
            self.cmd_history.scroll(event)
            self._restore_command()
            event.prevent_default()
            event.stop()

    def _restore_command(self) -> None:
        self.cmd_input.value = self.cmd_history.get_curr()
        self.cmd_input.cursor_position = len(self.cmd_input.value)


class ContextPane(Vertical):
    def __init__(self) -> None:
        super().__init__(id=WidgetID.CONTEXT_PANE)

    def compose(self) -> ComposeResult:
        yield Static(
            f'[{TextFormatting.TITLE}]{TuiText.CONTEXT}[/]\n'
            'Ready.\n'
            '↑ / ↓ Navigate command history.'
        )


class MainColumn(Vertical):
    DEFAULT_CSS = f'''
        {Terminal.__name__} {{
            height: 5fr;
            border: none;
             /*border: round;*/
            padding: 0;
            background: $surface;
        }}

        {ContextPane.__name__} {{
            height: 1fr;
        }}
    '''

    def __init__(self) -> None:
        super().__init__(
            id=WidgetID.MAIN_COLUMN,
            classes=WidgetClass.COLUMN,
        )

    def compose(self) -> ComposeResult:
        yield Static(f'[{TextFormatting.TITLE}]{TuiText.MAIN}[/]', classes=WidgetClass.TITLE)
        yield Terminal()
        yield HorizontalSplitter(classes=WidgetClass.SPLITTER)
        yield ContextPane()
