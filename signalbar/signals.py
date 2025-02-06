"""
Definitions for individual trits and symbols
"""

from enum import Enum
from typing import Tuple, List, Union

class Signal(Enum):
    """
    Defines the three possible states for a trit and provides tools for creating, printing, and
    parsing printed trits.
    """
    LOW = 0
    HIGH = 1
    BAR = 2

    @staticmethod
    def get_char(value: "Signal"):
        """
        Returns the character representation of a signal

        @param value: the signal to get the character for
        @return: the character that represents the signal
        @raise ValueError: the signal value isn't known
        """
        if value == Signal.LOW:
            return "▖"
        if value == Signal.HIGH:
            return "▘"
        if value == Signal.BAR:
            return "▌"
        raise ValueError("Unexpected signal value")

    @staticmethod
    def from_char(value: str):
        """
        Returns the signal given its character representation

        @param value: the character to get the signal for
        @return: the signal that the charactre represents
        @raise ValueError: the character isn't known
        """
        if value == "▖":
            return Signal.LOW
        if value == "▘":
            return Signal.HIGH
        if value == "▌":
            return Signal.BAR
        raise ValueError("Unexpected signal character")

    def __str__(self):
        return Signal.get_char(self)

    def __repr__(self):
        return Signal.get_char(self)

class Symbol():
    """
    Holds the representation of a single symbol
    """
    values: Tuple[Signal, ...]

    @staticmethod
    def _from_numstr(value: str):
        """
        Returns a symbol from a string-based numeric representation, i.e. "201" for BAR, LOW, HIGH

        @param value: The string to be turned into a symbol
        @return: The symbol the string represents
        @raise ValueError: The string has unrecognized characters
        """
        return tuple(Signal(int(char)) for char in value)

    def __init__(self, value: Union[str, Tuple[Signal, ...], List[Signal]]):
        """
        Make a new symbol from a either a string-based numeric representation, or a Signal tuple or
        Signal list

        Symbols are assumed the same if the hashes of their values are the same.

        @param value: The string, Tuple, or List to be turned into a symbol
        @return: The symbol that value represents
        @raise ValueError: The string has unrecognized characters, or value isn't a valid format
        """
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
