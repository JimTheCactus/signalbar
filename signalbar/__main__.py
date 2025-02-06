import logging
from sys import stderr

from .signalbar import encode_frame, decode_frame, Signal

logging.basicConfig(level=logging.INFO, stream=stderr)

in_array = input("Please enter the message to encode: ").encode("utf-8")
#in_array = "bob".encode("utf-8")
logging.debug("%s", in_array)
encoded_data = encode_frame(in_array)
result = list(encoded_data)
print("".join(str(x) for x in result))
# in_data = input("Please enter the signalbar code: ")
# result = [Signal.from_char(x) for x in in_data]
decoded_data = decode_frame(iter(result))
print(bytes(decoded_data).decode("utf-8"))
