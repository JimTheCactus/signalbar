from .signals import Signal, Symbol

_lookup_raw = [
    [
        "202", #0000
        "001", #0001
        "002", #0010
        "210", #0011
        "201", #0100
        "212", #0101
        "020", #0110
        "021", #0111
        "121", #1000
        "100", #1001
        "101", #1010
        "102", #1011
        "110", #1100
        "200", #1101
        "112", #1110
        "120", #1111
    ],
    [
        "210", #0000
        "001", #0001
        "002", #0010
        "011", #0011
        "010", #0100
        "201", #0101
        "020", #0110
        "021", #0111
        "200", #1000
        "100", #1001
        "101", #1010
        "102", #1011
        "212", #1100
        "012", #1101
        "202", #1110
        "120", #1111
    ],
    [
        "121", #0000
        "001", #0001
        "002", #0010
        "011", #0011
        "010", #0100
        "000", #0101
        "020", #0110
        "021", #0111
        "111", #1000
        "100", #1001
        "101", #1010
        "102", #1011
        "110", #1100
        "012", #1101
        "112", #1110
        "120", #1111
    ],
]

# Build the actual lookups we need from the lookup table constants
SIGNALBAR_SYMBOLS = [
    [
        Symbol(entry) for entry in table
    ]
    for table in _lookup_raw
]
SIGNALBAR_VALUES = [
    {
        value: key for key, value in enumerate(table)
    }
    for table in SIGNALBAR_SYMBOLS
]
SIGNALBAR_START = Symbol("220")
SIGNALBAR_END = Symbol("222")

