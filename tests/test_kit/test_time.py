import unittest

from mykit.kit.time import TimeFmt


## Note: The tests are using UTC timezone (for GitHub Actions VM)
# from datetime import datetime, timezone
# desired_date = datetime(2023, 8, 21, 15, 2, 3, tzinfo=timezone.utc)
# TS = desired_date.timestamp()
TS = 1692630123.0


class Test__TimeFmt(unittest.TestCase):

    def test_date(self):
        result = TimeFmt.date(TS)
        expected = 'Aug 21, 2023'
        self.assertEqual(result, expected)

    def test_hour(self):
        result = TimeFmt.hour(TS)
        expected = '15:02:03'
        self.assertEqual(result, expected)

    def test_sort(self):
        result = TimeFmt.sort(TS)
        expected = '20230821_150203'
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()