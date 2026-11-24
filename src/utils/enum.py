from enum import StrEnum


class IKebabCaseStrEnum(StrEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values) -> str:
        return name.lower().replace('_', '-')
