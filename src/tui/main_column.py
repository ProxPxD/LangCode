import pydash as _
from textual import events
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Input, RichLog, Static

from src.tui.const import TextFormatting, TuiText, WidgetClass, WidgetID
from src.tui.history import CmdHistory


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
        self.history = CmdHistory()

    def compose(self) -> ComposeResult:
        yield RichLog(wrap=True, markup=True, id=WidgetID.CMD_LOG)
        yield CmdLine()

    def _on_mount(self, event: events.Mount) -> None:
        self.cmd_input = self.query_one(f'#{WidgetID.CMD_INPUT}', Input)
        return super()._on_mount(event)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        command = event.value.strip()
        self.history.add(command)

    def _on_click(self, event: events.Click) -> None:
        self.cmd_input.focus()

    def on_key(self, event: events.Key) -> None:
        if event.key in {'up', 'down'}:
            self.history.scroll(event)
            self._restore_command()
            event.prevent_default()
            event.stop()

    def _restore_command(self) -> None:
        self.cmd_input.value = self.history.get_curr()
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
        yield ContextPane()
