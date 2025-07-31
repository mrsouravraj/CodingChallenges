import unittest
from resp import serialize, deserialize, RESPError

class TestRESPSerialization(unittest.TestCase):

    def test_serialize_array(self):
        self.assertEqual(serialize(["ping"]), "*1\r\n$4\r\nping\r\n")
        self.assertEqual(serialize(["echo", "hello world"]), "*2\r\n$4\r\necho\r\n$11\r\nhello world\r\n")
        self.assertEqual(serialize(["get", "key"]), "*2\r\n$3\r\nget\r\n$3\r\nkey\r\n")
        self.assertEqual(serialize(["set", "key", "value"]), "*3\r\n$3\r\nset\r\n$3\r\nkey\r\n$5\r\nvalue\r\n")

    def test_serialize_bulk_string(self):
        self.assertEqual(serialize(""), "$0\r\n\r\n")
        self.assertEqual(serialize(None), "$-1\r\n")

    def test_deserialize_simple_string(self):
        self.assertEqual(deserialize("+OK\r\n"), "OK")
        self.assertEqual(deserialize("+hello world\r\n"), "hello world")

    def test_deserialize_error(self):
        self.assertEqual(deserialize("-Error message\r\n"), {"error": "Error message"})

    def test_deserialize_integer(self):
        self.assertEqual(deserialize(":1000\r\n"), 1000)

    def test_deserialize_bulk_string(self):
        self.assertEqual(deserialize("$0\r\n\r\n"), "")
        self.assertEqual(deserialize("$-1\r\n"), None)
        self.assertEqual(deserialize("$5\r\nvalue\r\n"), "value")

    def test_deserialize_array(self):
        self.assertEqual(deserialize("*1\r\n$4\r\nping\r\n"), ["ping"])
        self.assertEqual(deserialize("*2\r\n$4\r\necho\r\n$11\r\nhello world\r\n"), ["echo", "hello world"])

    def test_deserialize_null_array(self):
        self.assertEqual(deserialize("*-1\r\n"), None)

    def test_invalid_cases(self):
        with self.assertRaises(RESPError):
            deserialize("~NotValid\r\n")

        with self.assertRaises(RESPError):
            deserialize("*2\r\n$3\r\nfoo\r\n")  # incomplete array
