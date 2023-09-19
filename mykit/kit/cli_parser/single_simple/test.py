import unittest

from mykit.kit.cli_parser.single_simple import Parser

from mykit.kit.stream_capture import StreamCapture


class Test__Parser(unittest.TestCase):

    def test_date(self):
        result = TimeFmt.date(self.timestamp, self.utc_offset)


if __name__ == '__main__':
    unittest.main()
