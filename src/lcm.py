import logging
from argparse import Namespace
from re import S

from src.cli import InputProcessor
from src.cli.const import Cmd
from src.loading import LoaderKind, LoaderProvider

# from cli.outer_cli import Modes, OuterCLI
# from context.context import Context
# from logic.conf.fcn import FCN
# from logic.db import GDM, LoginData
# from logic.sci import SCI
# from loop_mging.input_mgr import InputMgr
lazy from src.loading.abstract_loaders import Loader
lazy from src.tui import Tui


logger = logging.getLogger(__name__)


class LCM:
    """
    Lang Code Manager
    """
    def __init__(self, *, log = None) -> None:
        self.loader: Loader = LoaderProvider.get_for(LoaderKind.ALL)
        self.input_processor = InputProcessor(is_tui=False)
        self.tui: Tui | None = None
        ...
        # self.outer_cli = OuterCLI()
        # self.input_mgr = InputMgr()
        # self.gdm: GDM = GDM(log)
        # self.fcn = FCN()
        # self.sci: SCI = SCI()
        # self.context = Context()

    def run(self) -> None:
        parsed: Namespace = self.input_processor.process()  # TODO: add a proper application context
        match parsed.cmd:
            case Cmd.TUI:
                self.tui = Tui()
                self.tui.run()
            case _: raise ValueError(f'Unrecognized command: {parsed.cmd}')
