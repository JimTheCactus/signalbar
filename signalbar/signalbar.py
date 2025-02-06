# ▖▘▌
"""
signalbar

A library for generating and decoding signalbar barcodes
"""
from typing import Iterable, Iterator
import logging

from .signals import Signal, Symbol
from .lookuptable import SIGNALBAR_SYMBOLS, SIGNALBAR_VALUES, SIGNALBAR_START, SIGNALBAR_END

class FramingError(ValueError):
    """ The framing of the message was incorrect """

class DecodingError(ValueError):
    """ The data contained information that could not be decoded correctly """

class EndOfMessage(StopIteration):
    """ The end of the message was reached """

logger = logging.getLogger(__name__)

def encode_nibble(nibble: int, last_value: Signal) -> Symbol:
    """
    Encodes a single nibble into a symbol

    @param nibble: An integer from 0 to 15 inclusive to be encoded
    @param last_value: The signal value at the end of the last symbol
    @return: The encoded symbol value
    @raise KeyError: The last_value or the nibble are out of range
    """
    logger.debug("%s, %s", nibble, last_value)
    return SIGNALBAR_SYMBOLS[last_value.value][nibble]

def encode_bytes(msg: bytes, initial_last_value: Signal) -> Iterator[Symbol]:
    """
    Encodes a bytes structure into symbols

    @param msg: A bytes structure to be encoded
    @param initial_last_value: The signal value at the end of the last symbol
    @return: A generator that returns a sequence of Symbols
    @raise KeyError: The last_value or the nibble are out of range
    """
    last_value = initial_last_value
    for byte in msg:
        result = encode_nibble(byte >> 4, last_value)
        yield result
        last_value =  result.values[-1]
        result = encode_nibble(byte & 0xF, last_value)
        yield result
        last_value =  result.values[-1]

def symbol_to_signals(value: Symbol) -> Iterator[Signal]:
    """
    Transforms a symbol into the individual signals that make it up

    @param value: A symbol to be deconstructued into it's signals
    @return: A generator that returns the symbol's signals
    """
    yield from value.values

def encode_frame(msg: bytes)  -> Iterator[Signal]:
    """
    Encodes a sequence of bytes into a sequence of signals

    @param msg: A bytes structure that contains the data to be framed and encoded
    @return: A generator that returns the signals that represent that bytes structure
    @raise KeyError: The last_value or the nibble are out of range
    """
    # Include frame header
    yield from SIGNALBAR_START.values
    # Include encoded data
    for x in encode_bytes(msg, Signal.LOW):
        yield from symbol_to_signals(x)
    # Include frame footer
    yield from SIGNALBAR_END.values

def decode_bytes(msg: Iterable[Signal], last_value: Signal) \
    -> Iterator[int]:
    """
    Decodes a sequence of signals into bytes

    @param msg: An iteratble that holds an END symbol terminated signal sequence
    @param last_value: The signal value at the end of the last symbol
    @return: A generator that returns the decoded byte information
    @raise DecodingError: The data was unreadable
    """
    while True:
        try:
            symbol1 = Symbol((next(msg),next(msg),next(msg)))
        except StopIteration as exc:
            raise DecodingError("Byte contained the incorrect number of trits.") from exc
        logger.debug("%s", symbol1)
        if symbol1 == SIGNALBAR_END:
            logger.debug("Done decoding.")
            return
        try:
            nibble1 = SIGNALBAR_VALUES[last_value.value][symbol1]
        except KeyError as exc:
            raise DecodingError(
                f"Encountered invalid symbol {symbol1} with last signal {last_value}.",
            ) from exc
        last_value = symbol1.values[-1]
        try:
            symbol2 = Symbol((next(msg),next(msg),next(msg)))
        except StopIteration as exc:
            raise DecodingError("Byte contained the incorrect number of trits.") from exc
        logger.debug("%s", symbol2)
        if symbol2 == SIGNALBAR_END:
            raise DecodingError("Byte contained the incorrect number of trits.")
        try:
            nibble2 = SIGNALBAR_VALUES[last_value.value][symbol2]
        except KeyError as exc:
            raise DecodingError(
                f"Encountered invalid symbol {symbol2} with last signal {last_value}."
            ) from exc
        data = nibble1<<4 | nibble2
        logger.debug("%s", data)
        yield data
        last_value = symbol2.values[-1]

def decode_frame(msg: Iterable[Signal]) -> Iterator[int]:
    """
    Locates the beginning of a frame and then decodes it into the contained message

    @param msg: An iteratble that holds a START symbol, data, and END symbol terminated signal
    sequence
    @return: A generator that returns the decoded byte information
    @raise DecodingError: The data was unreadable
    """
    initial_trits = [next(msg),next(msg),next(msg)]
    while True:
        symbol = Symbol(initial_trits)
        if symbol == SIGNALBAR_START:
            break
        try:
            initial_trits.pop(0)
            initial_trits.append(next(msg))
        except StopIteration as exc:
            raise FramingError("Unable to find start sequence!") from exc
    return decode_bytes(msg, Signal.LOW)
