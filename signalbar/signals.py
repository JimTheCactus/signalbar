from enum import Enum
from typing import Tuple, List

class Signal(Enum):
    LOW = 0
    HIGH = 1
    BAR = 2

    @staticmethod
    def get_char(value: "Signal"):
        if value == Signal.LOW:
            return "▖"
        elif value == Signal.HIGH:
            return "▘"
        elif value == Signal.BAR:
            return "▌"
        else:
            raise ValueError("Unexpected signal value")

    @staticmethod
    def from_char(value: str):
        if value == "▖":
            return Signal.LOW
        elif value == "▘":
            return Signal.HIGH
        elif value == "▌":
            return Signal.BAR
        else:
            raise ValueError("Unexpected signal character")

    def __str__(self):
        return Signal.get_char(self)

    def __repr__(self):
        return Signal.get_char(self)

class Symbol():
    values: Tuple[Signal]

    @staticmethod
    def _from_numstr(value: str):
        return tuple(Signal(int(char)) for char in value)

    def __init__(self, value: str | Tuple[Signal] | List[Signal]):
        if isinstance(value, list):
            self.values = tuple(iter(value))
        elif isinstance(value, tuple):
            self.values = value
        elif isinstance(value, str):
            self.values = Symbol._from_numstr(value)
        else:
            raise ValueError("Input must be string or list of symbols")

    def __hash__(self):
        return hash(self.values)

    def __repr__(self):
        return "".join(Signal.get_char(x) for x in self.values)

    def __str__(self):
        return "".join(Signal.get_char(x) for x in self.values)

    def __eq__(self, value):
        if not isinstance(value, Symbol):
            raise ValueError("Can't compare against non-Symbols")
        return hash(self) == hash(value)

