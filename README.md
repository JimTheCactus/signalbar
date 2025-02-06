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

#### 3-bits-to-2 trit

This encoding has an efficiency of 88.8%

* 0: 000 00
* 1: 001 01
* 2: 010 02
* 3: 011 10
* 4: 100 11
* 5: 101 12
* 6: 110 20
* 7: 111 21
* 8: N/A 22 - Control symbol

#### 4-bits-to-3 trit
NANA 22X - Control
Rightside up:  ▌▌▖<data> ▌▌▌
Upside down:   ▌▌▌<data> ▘▌▌
Mirrored:      ▌▌▌<data> ▖▌▌
Rotate+Mirror: ▌▌▘<data> ▌▌▌

The very first symbol assumes 0 as the trailing character

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

