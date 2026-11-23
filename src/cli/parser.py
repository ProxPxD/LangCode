from argparse import ArgumentParser


class ParserBuilder:
    @classmethod
    def build(cls, *, is_tui: bool) -> ArgumentParser:
        ...
