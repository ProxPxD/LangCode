from textual.widgets import Input, RichLog
from textual_widgets import HorizontalSplitter, VerticalSplitter

from .const import WidgetClass, WidgetID

TUI_CSS = CSS = f'''
{VerticalSplitter.__name__} {{
    height: 100%;
    width: 1;
}}

{HorizontalSplitter.__name__} {{
    height: 1;
    width: 100%;
}}

.{WidgetClass.SPLITTER}:hover,
.{WidgetClass.SPLITTER}.dragging {{
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
