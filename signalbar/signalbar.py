# ▖▘▌
from typing import Tuple
from collections.abc import Generator, Iterable
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
    logger.debug("%s, %s", nibble, last_value)
    return SIGNALBAR_SYMBOLS[last_value.value][nibble]

def encode_bytes(msg: bytes, initial_last_value: Signal) -> Generator[Symbol, None, None]:
    last_value = initial_last_value
    for byte in msg:
        result = encode_nibble(byte >> 4, last_value)
        yield result
        result = encode_nibble(byte & 0xF, result.values[-1])
        yield result

def symbol_to_signals(value: Symbol) -> Generator[Signal, None, None]:
    yield from value.values

def encode_frame(msg: bytes)  -> Generator[Signal, None, None]:
    # Include frame header
    yield from SIGNALBAR_START.values
    # Include encoded data
    for x in encode_bytes(msg, Signal.LOW):
        yield from symbol_to_signals(x)
    # Include frame footer
    yield from SIGNALBAR_END.values

def decode_bytes(msg: Iterable[Signal], last_value: Signal) \
    -> Generator[Tuple[int, Signal], None, None]:
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
                f"Encountered invalid symbol {symbol2} with last signal {last_value}.",
            ) from exc
        try:
            symbol2 = Symbol((next(msg),next(msg),next(msg)))
        except StopIteration as exc:
            raise DecodingError("Byte contained the incorrect number of trits.") from exc
        logger.debug("%s", symbol2)
        if symbol2 == SIGNALBAR_END:
            raise DecodingError("Byte contained the incorrect number of trits.")
        try:
            nibble2 = SIGNALBAR_VALUES[symbol1.values[-1].value][symbol2]
        except KeyError as exc:
            raise DecodingError(
                f"Encountered invalid symbol {symbol2} with last signal {last_value}."
            ) from exc
        yield (nibble1<<4 | nibble2, symbol1.values[-1])


def decode_data(msg: Iterable[Signal], initial_last_value: Signal):
    last_value = initial_last_value
    for data in decode_bytes(msg, last_value):
        logger.debug("%s", data)
        last_value = data[1]
        yield data[0]

def decode_frame(msg: Iterable[Signal]) -> Generator[int]:
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
    return decode_data(msg, Signal.LOW)
