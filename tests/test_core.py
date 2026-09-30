import unittest

from i_so_8859_1_decoder import decode, encode, lookup_table, reverse_table


class TestDecode(unittest.TestCase):
    def test_empty_bytes(self):
        self.assertEqual(decode(b""), "")

    def test_ascii(self):
        self.assertEqual(decode(b"Hello"), "Hello")

    def test_high_bytes_identity(self):
        # Every byte value maps to the code point of the same number.
        self.assertEqual(decode(bytes(range(256))), "".join(chr(i) for i in range(256)))

    def test_single_byte(self):
        self.assertEqual(decode(b"\xff"), "\u00ff")

    def test_bytearray_accepted(self):
        self.assertEqual(decode(bytearray(b"ABC")), "ABC")

    def test_non_bytes_raises_type_error(self):
        with self.assertRaises(TypeError):
            decode("not bytes")
        with self.assertRaises(TypeError):
            decode(None)


class TestEncode(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(encode(""), b"")

    def test_ascii(self):
        self.assertEqual(encode("Hello"), b"Hello")

    def test_full_range(self):
        self.assertEqual(encode("".join(chr(i) for i in range(256))), bytes(range(256)))

    def test_high_code_point(self):
        self.assertEqual(encode("\u00ff"), b"\xff")

    def test_out_of_range_raises_value_error(self):
        with self.assertRaises(ValueError):
            encode("\u0100")

    def test_out_of_range_error_mentions_index(self):
        try:
            encode("AB\u0100CD")
        except ValueError as exc:
            self.assertIn("index 2", str(exc))
        else:
            self.fail("expected ValueError")

    def test_non_str_raises_type_error(self):
        with self.assertRaises(TypeError):
            encode(b"not a string")
        with self.assertRaises(TypeError):
            encode(None)

    def test_round_trip(self):
        original = "".join(chr(i) for i in range(256))
        self.assertEqual(decode(encode(original)), original)


class TestTables(unittest.TestCase):
    def test_lookup_table_length(self):
        self.assertEqual(len(lookup_table), 256)

    def test_lookup_table_identity(self):
        for i, ch in enumerate(lookup_table):
            self.assertEqual(ord(ch), i)

    def test_reverse_table_length(self):
        self.assertEqual(len(reverse_table), 256)

    def test_reverse_table_inverse(self):
        for ch, byte_val in reverse_table.items():
            self.assertEqual(lookup_table[byte_val], ch)


if __name__ == "__main__":
    unittest.main()
