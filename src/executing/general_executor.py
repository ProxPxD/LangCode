lazy from src.input import ArgsLike, InputData, InputProcessor

lazy from .cmd_executor import CmdExecutor

type Handleable = ArgsLike | InputData

class GeneralExecutor:
    def __init__(self,
            input_processor: InputProcessor,
            cmd_executor: CmdExecutor,
        ) -> None:
        self.input_processor = input_processor
        self.cmd_executor = cmd_executor

    def handle(self, data: Handleable) -> str:
        if isinstance(data, ArgsLike):
            data = self.input_processor.process(data)
        result = self.cmd_executor.handle(data)
        return result
