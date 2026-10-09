# ISO 8859-1 Decoder

Decodes and encodes text using the ISO 8859-1 (Latin-1) character set — the standard byte-for-byte mapping where code point U+00NN corresponds to byte 0xNN.

```python
from i_so_8859_1_decoder import decode, encode, lookup_table, reverse_table

text = decode(b"caf\xe9")       # 'café'
back = encode(text)             # b'caf\xe9'
first_char_byte = reverse_table['é']  # 233
```

## Why this exists

Python's built-in `'latin-1'` codec already does this job. This library provides a named, typed API around it for projects that prefer explicit function calls over passing codec name strings, and exposes the full 256-entry lookup and reverse tables for direct code-point-to-byte mapping.

The one edge worth knowing: encoding a string containing any code point above U+00FF raises `ValueError` with the index of the offending character. Every byte value is valid on the decode side, so `decode` only fails on non-bytes input.

## Performance

The window keeps a bounded buffer, so `push` is constant time and memory does not
grow with the length of the stream. `peak` and `trough` are linear in the window
size, which is the trade that keeps `push` cheap.

## Limitations

Values are coerced to floats, so very large integers lose precision. If you need
exact integer aggregates over a window, this is the wrong tool.

