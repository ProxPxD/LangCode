from venv import logger

lazy from src.input import ArgsLike, InputData, InputProcessor

lazy from .cmd_executor import CmdExecutor

type Handleable = ArgsLike | InputData


class GeneralExecutor:
    def __init__(self,
            input_processor: InputProcessor,
            cmd_executor: CmdExecutor,
        ) -> None:
        self.input_processor = input_processor

    def _ensure_input_data(self, data: Handleable) -> InputData:
        if isinstance(data, (str, list)):
            data = self.input_processor.process(data)
        return data

    def handle(self, data: Handleable) -> str:
        input_data = self._ensure_input_data(data)
        if input_data.help:
            return self._return_help(input_data)
        return NotImplemented

    def _return_help(self, input_data: InputData) -> str:
        tree = self.input_processor.parser_tree
        for cmd in filter(bool, input_data.cmds):
            tree = tree.subparsers[cmd]
        return tree.parser.format_help()
