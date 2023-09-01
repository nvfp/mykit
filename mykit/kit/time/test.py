import unittest

from mykit.kit.time import TimeFmt


class Test__TimeFmt(unittest.TestCase):

    def setUp(self):
        self.timestamp = 1692630123.0
        self.utc_offset = 0

    def test_date(self):
        result = TimeFmt.date(self.timestamp, self.utc_offset)
        expected = 'Aug 21, 2023'
        self.assertEqual(result, expected)

    def test_hour(self):
        result = TimeFmt.hour(self.timestamp, self.utc_offset)
        expected = '15:02:03'
        self.assertEqual(result, expected)

    def test_sort(self):
        result = TimeFmt.sort(self.timestamp, self.utc_offset)
        expected = '20230821_150203'
        self.assertEqual(result, expected)

    def test_neat(self):
        result = TimeFmt.neat(self.timestamp, self.utc_offset)
        expected = '2023 Aug 21, 15:02:03 UTC+0000'
        self.assertEqual(result, expected)

        result = TimeFmt.neat(self.timestamp, 1.75)
        expected = '2023 Aug 21, 16:47:03 UTC+0145'
        self.assertEqual(result, expected)

        result = TimeFmt.neat(self.timestamp, -11.15)
        expected = '2023 Aug 21, 03:53:03 UTC-1109'
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()