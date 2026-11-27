import logging
import sys

from src.input import InputProcessor
from src.input.const import Cmd
lazy from src.executing import CmdExecutor, GeneralExecutor
lazy from src.input.input_data import InputData
lazy from src.loading import Loader, LoaderKind, LoaderProvider
lazy from src.tui import Tui

# from cli.outer_cli import Modes, OuterCLI
# from context.context import Context
# from logic.conf.fcn import FCN
# from logic.db import GDM, LoginData
# from logic.sci import SCI
# from loop_mging.input_mgr import InputMgr
        # ...
        # self.outer_cli = OuterCLI()
        # self.input_mgr = InputMgr()
        # self.gdm: GDM = GDM(log)
        # self.fcn = FCN()
        # self.sci: SCI = SCI()
        # self.context = Context()


logger = logging.getLogger(__name__)


class AppManager:
    def __init__(self, *, log = None) -> None:
        self.input_processor = InputProcessor(is_tui=False)
        self._executor: GeneralExecutor | None = None
        self._tui: Tui | None = None
        self._loader: Loader | None = None

    @property
    def executor(self) -> GeneralExecutor:
        if self._executor is None:
            self._executor = GeneralExecutor(
                input_processor=self.input_processor,
                cmd_executor=CmdExecutor(),
            )
        return self._executor

    @property
    def tui(self) -> Tui:
        if not self._tui:
            self._tui = Tui(
                input_handler=GeneralExecutor(
                    input_processor=InputProcessor(is_tui=True),
                    cmd_executor=CmdExecutor(),
                ),
            )
        return self._tui

    @property
    def loader(self) -> Loader:
        if self._loader is None:
            self._loader = LoaderProvider.get_for(LoaderKind.ALL)
        return self._loader  # pyright: ignore[reportReturnType]  # TODO: remove when support starts or LS is changed

    def run(self) -> None:
        input_data: InputData = self.input_processor.process()  # TODO: add a proper application context
        match input_data.cmd:
            case Cmd.TUI:
                logger.debug('Starting TUI')
                self.tui.run()
            case Cmd(): print(self.executor.handle(input_data), file=sys.stdout)
            case None if input_data.error: print(input_data.error.message, file=sys.stdout)
            case _: raise ValueError(f'Unrecognized command: {input_data.cmd}')
