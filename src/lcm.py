import logging
from argparse import Namespace
from re import S

# from cli.outer_cli import Modes, OuterCLI
# from context.context import Context
from loading import LoaderKind, LoaderProvider
# from logic.conf.fcn import FCN
# from logic.db import GDM, LoginData
# from logic.sci import SCI
# from loop_mging.input_mgr import InputMgr
lazy from loading.abstract_loaders import Loader
from src.tui.app import TerminalTUI


class LCM:
    """
    Lang Code Manager
    """
    def __init__(self, *, log = None) -> None:
        self.loader: Loader = LoaderProvider.get_for(LoaderKind.ALL)
        self.tui = TerminalTUI()
        ...
        # self.outer_cli = OuterCLI()
        # self.input_mgr = InputMgr()
        # self.gdm: GDM = GDM(log)
        # self.fcn = FCN()
        # self.sci: SCI = SCI()
        # self.context = Context()

    def run(self) -> None:
        self.tui.run()
        return
        parsed: Namespace = self.outer_cli.parse()  # TODO: add a proper application context
        match parsed.cmd:
            case Modes.start: self.run_loop()
            case Modes.query: self.run_rdf(parsed.rdf)
            case Modes.load: self.run_load(parsed.load)
            case _: raise ValueError(f'Unrecognized command: {parsed.cmd}')

    def run_loop(self) -> None:
        logging.debug('Run Loop')
        self.input_mgr.parse()
        ...
        # while self.context.loop:
        #     self.run_single(shlex.split(input()))

    def run_rdf(self, rdf_parsed) -> None:
        logging.debug('Run RDF')
        res = self.gdm.raw_query(rdf_parsed.query)
        print(res)

    def run_load(self, load_parsed) -> None:
        logging.debug('Run Load')
        # TODO: Nun supozu unu bazon
        conf = GenLoader.load(load_parsed.file)
        normed = self.fcn.norm(conf)
        generateds = self.sci.interpret(normed)
