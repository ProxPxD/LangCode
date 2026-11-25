import logging

from src.input import InputProcessor
from src.input.const import Cmd
lazy from src.executing import Executor
lazy from src.input.input_data import InputData
lazy from src.loading import Loader, LoaderKind, LoaderProvider
lazy from src.tui import Tui

# from cli.outer_cli import Modes, OuterCLI
# from context.context import Context
# from logic.conf.fcn import FCN
# from logic.db import GDM, LoginData
# from logic.sci import SCI
# from loop_mging.input_mgr import InputMgr


logger = logging.getLogger(__name__)


class AppManager:
    def __init__(self, *, log = None) -> None:
        self.input_processor = InputProcessor(is_tui=False)
        self._executor = Executor()
        self._tui: Tui | None = None
        self._loader: Loader | None = None
        ...
        # self.outer_cli = OuterCLI()
        # self.input_mgr = InputMgr()
        # self.gdm: GDM = GDM(log)
        # self.fcn = FCN()
        # self.sci: SCI = SCI()
        # self.context = Context()

    @property
    def tui(self) -> Tui:
        if not self._tui:
            self._tui = Tui()
        return self._tui

    @property
    def loader(self) -> Loader:
        if self._loader is None:
            self._loader = LoaderProvider.get_for(LoaderKind.ALL)
        return self._loader  # pyright: ignore[reportReturnType]  # TODO: remove when support starts or LS is changed

    def run(self) -> None:
        parsed: InputData = self.input_processor.process()  # TODO: add a proper application context
        match parsed.cmd:
            case Cmd.TUI:
                logger.debug('Starting TUI')
                self.tui.run()
            case _: raise ValueError(f'Unrecognized command: {parsed.cmd}')
