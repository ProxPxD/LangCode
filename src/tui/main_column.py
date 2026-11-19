from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Input, RichLog, Static

from src.tui.const import TextFormatting, TuiText, WidgetClass, WidgetID


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
        #{WidgetID.CMD_HISTORY} {{
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

    def compose(self) -> ComposeResult:
        yield RichLog(wrap=True, markup=True, id=WidgetID.CMD_HISTORY)
        yield CmdLine()

class ConsolePane(Vertical):
    DEFAULT_CSS = f'''
        {Terminal.__name__} {{
            /*border: round;*/
        }}

    '''
    def compose(self) -> ComposeResult:
        yield Static(f'[{TextFormatting.TITLE}]{TuiText.MAIN}[/]', classes=WidgetClass.TITLE)
        yield Terminal()

class ContextPane(Vertical):
    DEFAULT_CSS = f'''
        {ConsolePane.__name__} {{
            border: none;
            padding: 0;
            background: $surface;
        }}
    '''
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
        {ConsolePane.__name__} {{
            height: 5fr;
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
        yield ConsolePane()
        yield ContextPane()
