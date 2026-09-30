"""ISO 8859-1 (Latin-1) decoder and encoder.

Exposes ``decode`` and ``encode`` for converting between bytes and
``str`` using the ISO 8859-1 character set, plus a ``lookup_table``
and ``reverse_table`` for direct code-point mapping.
"""

from .core import decode, encode, lookup_table, reverse_table

__all__ = ["decode", "encode", "lookup_table", "reverse_table"]
