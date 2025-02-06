# Signal Bar

Uses the unicode symbols ▖, ▘, and ▌ to encode data in a way that can be recovered optically.

Credit to [vo1dlabs](https://github.com/v01dlabs) and [dollcode](https://github.com/v01dlabs/dollcode)
for some of the seed ideas an initial implementation motivation.

## Sections

* Protocol
    * Signals
    * Symbols
    * Frames

## Protocol

### Signals

* All data will be encoded using terinary values:
    * 0: ▖
    * 1: ▘
    * 2: ▌
* No other signals will be used (i.e. there is no data encoded using whitespace.)

### Symbols

Data is encoded using 4 bits to 3 trits. A double 2 indicates a control message and should never
appear in encoded data. The symbols have been selected to guarantee a maximum run length of a
single symbol of 5. The presence of a 6 symbol run is sufficient to know that the message is
corrupt. Also, since the trailing signal of the previous symbol dictates the next symbol, if
an error in decoding has occured, there is a chance that invalid symbols can be encountered. As
such, if an invalid symbol is encountered, the message can be known to be corrupted before that
point in the decoding.

```
Trailing Character 0
    NRUN 000
    0001 001
    0010 002
    XXXX 010
    XXXX 011
    XXXX 012
    0110 020
    0111 021
    CTRL 022
    1001 100
    1010 101
    1011 102
    1100 110
    XXXX 111
    1110 112
    1111 120
    1000 121
    CTRL 122
    1101 200
    0100 201
    0000 202
    0011 210
    XXXX 211
    0101 212
    CTRL 220 - If uninitialized: Begin Bar
    CTRL 221 - If uninitialized: Flip Vertical, Restart
    CTRL 222 - If uninitialized: Flip Horizontal, Restart. Else: End of Sequence

Trailing Character 1
    XXXX 000
    0001 001
    0010 002
    0100 010
    0011 011
    1101 012
    0110 020
    0111 021
    CTRL 022
    1001 100
    1010 101
    1011 102
    XXXX 110
    NRUN 111
    XXXX 112
    1111 120
    XXXX 121
    CTRL 122
    1000 200
    0101 201
    1110 202
    0000 210
    XXXX 211
    1100 212
    CTRL 220
    CTRL 221
    CTRL 222 - If uninitialized: Flip Horizontal, Restart. Else: End of Sequence

Trailing Character 2
    0101 000
    0001 001
    0010 002
    0100 010
    0011 011
    1101 012
    0110 020
    0111 021
    CTRL 022
    1001 100
    1010 101
    1011 102
    1100 110
    1000 111
    1110 112
    1111 120
    0000 121
    CTRL 122
    CTRL 200
    CTRL 201
    CTRL 202
    CTRL 210
    CTRL 211
    CTRL 212
    CTRL 220
    CTRL 221
    NRUN 222 - If uninitialized: Flip Horizontal, Restart. Else: End of Sequence
```

### Frames

Frames always begin with a 220 sequence and end with a 222 sequence. The very first symbol in the
data assumes that the trailing character of the previous symbol was a 0, which following a 220
start-of-frame sequence is correct.

The choice of control symbols is to make it possible to decode signalbar in any orientation, and
also in mirrored conditions.

```
Rightside up:  ▌▌▖<data> ▌▌▌
Upside down:   ▌▌▌<data> ▘▌▌
Mirrored:      ▌▌▌<data> ▖▌▌
Rotate+Mirror: ▌▌▘<data> ▌▌▌
```
