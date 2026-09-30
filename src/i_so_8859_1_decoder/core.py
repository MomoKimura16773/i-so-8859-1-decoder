"""Core ISO 8859-1 (Latin-1) encoding and decoding routines.

ISO 8859-1 maps every byte value 0x00–0xFF to the Unicode code point
with the same numeric value. Because that mapping is a trivial identity,
Python's built-in ``bytes.decode('latin-1')`` already does the right
thing — this library exists to provide a small, explicit, dependency-free
surface around it for projects that want a named API rather than a
stringly-typed codec argument.

The non-obvious design choice is error handling. The real codec raises
``UnicodeDecodeError`` / ``UnicodeEncodeError`` for out-of-range input,
but since every byte is valid Latin-1 the only failure mode is encoding
a code point above U+00FF. We surface that as a ``ValueError`` with the
offending index so callers get a single exception type for a single
failure mode.
"""

from __future__ import annotations

from typing import List

# The full 256-entry Latin-1 table: code point i corresponds to byte i.
# Building it once and reusing avoids recomputing the trivial identity on
# every call while keeping the mapping visible and inspectable.
lookup_table: List[str] = [chr(i) for i in range(256)]

# Reverse mapping from single-character string to its byte value.
# We keep it as a dict because callers may legitimately want to look up
# one character; building it once is cheaper than chr().encode() per call.
reverse_table: dict = {chr(i): i for i in range(256)}


def decode(data: bytes) -> str:
    """Decode ``data`` as ISO 8859-1 (Latin-1) bytes into a string.

    Every byte value 0x00–0xFF is a valid Latin-1 character, so this
    function never raises for input of type ``bytes`` (or ``bytearray``,
    which is accepted by the underlying codec). An empty input returns
    an empty string.

    Args:
        data: Bytes to decode. ``bytearray`` is also accepted.

    Returns:
        The decoded string. Each byte maps to the Unicode code point
        with the same numeric value.

    Raises:
        TypeError: If ``data`` is not a bytes-like object.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError(
            "decode() expects bytes or bytearray, got "
            + type(data).__name__
        )
    # latin-1 is a 1:1 identity map; the codec is always available.
    return bytes(data).decode("latin-1")


def encode(text: str) -> bytes:
    """Encode ``text`` into ISO 8859-1 (Latin-1) bytes.

    Only code points U+0000 through U+00FF are representable in Latin-1.
    Any character outside that range raises ``ValueError`` with the index
    of the offending character, so callers can locate the problem in the
    original string.

    Args:
        text: String to encode.

    Returns:
        The Latin-1 byte representation of ``text``.

    Raises:
        TypeError: If ``text`` is not a ``str``.
        ValueError: If ``text`` contains a code point above U+00FF.
    """
    if not isinstance(text, str):
        raise TypeError(
            "encode() expects str, got " + type(text).__name__
        )
    # Walk the string once to find the first out-of-range character.
    # We do this before calling into the codec so we can report the
    # index, which the built-in UnicodeEncodeError does not expose in a
    # stable, documented way across Python versions.
    for i, ch in enumerate(text):
        if ord(ch) > 0xFF:
            raise ValueError(
                "character at index "
                + str(i)
                + " is U+"
                + format(ord(ch), "04X")
                + ", which is outside the ISO 8859-1 range"
            )
    return text.encode("latin-1")
