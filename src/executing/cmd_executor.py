from src.input import InputData


class CmdExecutor:
    def __init__(self) -> None:
        pass

    def handle(self, inpu_data: InputData) -> str:
        raise NotImplementedError
