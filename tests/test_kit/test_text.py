import unittest

from mykit.kit.text import connum, in_byte, num_approx, num_round


class Test__connum(unittest.TestCase):

    def test(self):

        self.assertEqual(connum(0), '0')
        self.assertEqual(connum(0.0), '0')
        self.assertEqual(connum('0'), '0')
        
        self.assertEqual(connum(-0), '0')
        self.assertEqual(connum(-0.0), '0')
        self.assertEqual(connum('-0'), '0')
        self.assertEqual(connum('-0.0'), '0')
        
        self.assertEqual(connum('1.0'), '1')
        self.assertEqual(connum('+1.0'), '1')
        self.assertEqual(connum('001.0'), '1')
        self.assertEqual(connum('001.0000'), '1')

        self.assertEqual(connum(1.250), '1.25')
        self.assertEqual(connum('-1.250'), '-1.25')

        self.assertEqual(connum(0.1010), '0.101')
        self.assertEqual(connum(-0.100), '-0.1')

        self.assertEqual(connum(0.0003), '0.0003')
        self.assertEqual(connum(0.000300000), '0.0003')
        self.assertEqual(connum(-0.000300000), '-0.0003')
        self.assertEqual(connum('+0.000000300000'), '0.0000003')

        with self.assertRaises(ValueError) as ctx: connum('foo')
        self.assertEqual(str(ctx.exception), "Invalid numeric input: 'foo'.")

        with self.assertRaises(ValueError) as ctx: connum([1,2,3])
        self.assertEqual(str(ctx.exception), "Invalid numeric input: [1, 2, 3].")


class Test__in_byte(unittest.TestCase):

    def test_default(self):

        self.assertEqual(in_byte(0), '0 B')
        self.assertEqual(in_byte(-1), '-1 B')
        self.assertEqual(in_byte(1), '1 B')
        self.assertEqual(in_byte(-100), '-100 B')
        self.assertEqual(in_byte(100), '100 B')
        
        self.assertEqual(in_byte(1024), '1 KiB')
        self.assertEqual(in_byte(1025), '1 KiB')
        
        self.assertEqual(in_byte(1100), '1.07 KiB')
        self.assertEqual(in_byte(-99999), '-97.66 KiB')
        
        self.assertEqual(in_byte(-555599999.24100), '-529.86 MiB')

    def test_precision(self):

        result = in_byte(1, precision=0)
        expected = '1 B'
        self.assertEqual(result, expected)

        result = in_byte(1, precision=1)
        expected = '1 B'
        self.assertEqual(result, expected)

        result = in_byte(1, precision=2)
        expected = '1 B'
        self.assertEqual(result, expected)

        result = in_byte(1.3, precision=2)
        expected = '1 B'
        self.assertEqual(result, expected)

        result = in_byte(1200, precision=0)
        expected = '1 KiB'
        self.assertEqual(result, expected)

        result = in_byte(1800, precision=0)
        expected = '2 KiB'
        self.assertEqual(result, expected)

        result = in_byte(12345, precision=0)
        expected = '12 KiB'
        self.assertEqual(result, expected)

        result = in_byte(12345, precision=1)
        expected = '12.1 KiB'
        self.assertEqual(result, expected)

        result = in_byte(12345, precision=7)
        expected = '12.0556641 KiB'
        self.assertEqual(result, expected)

        result = in_byte(-900800700600, precision=3)
        expected = '-838.936 GiB'
        self.assertEqual(result, expected)

        result = in_byte(100200300400500600, precision=0)
        expected = '89 PiB'
        self.assertEqual(result, expected)

    def test_gap(self):

        result = in_byte(0, gap=0)
        expected = '0B'
        self.assertEqual(result, expected)

        result = in_byte(1, gap=0)
        expected = '1B'
        self.assertEqual(result, expected)

        result = in_byte(123456789, gap=0)
        expected = '117.74MiB'
        self.assertEqual(result, expected)

        result = in_byte(9876, gap=1)
        expected = '9.64 KiB'
        self.assertEqual(result, expected)

        result = in_byte(100200300, gap=3)
        expected = '95.56   MiB'
        self.assertEqual(result, expected)

        result = in_byte(99999999999, gap=7)
        expected = '93.13       GiB'
        self.assertEqual(result, expected)


class Test__num_approx(unittest.TestCase):

    def test_default(self):

        self.assertEqual(num_approx(0), '0')
        self.assertEqual(num_approx(1), '1')
        self.assertEqual(num_approx(-1), '-1')
        self.assertEqual(num_approx(3), '3')

        self.assertEqual(num_approx(17), '17')
        self.assertEqual(num_approx(333), '333')
        self.assertEqual(num_approx(999), '999')
        self.assertEqual(num_approx(-999), '-999')
        self.assertEqual(num_approx(-124.12), '-124.1')

        self.assertEqual(num_approx(1000), '1K')
        self.assertEqual(num_approx(1001), '1K')
        self.assertEqual(num_approx(1049), '1K')
        self.assertEqual(num_approx(1050), '1.1K')
        self.assertEqual(num_approx(1099), '1.1K')
        self.assertEqual(num_approx(1399), '1.4K')
        self.assertEqual(num_approx(-1399), '-1.4K')

        self.assertEqual(num_approx(999_000_000), '999M')
        self.assertEqual(num_approx(1_200_000_000), '1.2B')
        self.assertEqual(num_approx(356_351_352_642_742), '356.4T')
        self.assertEqual(num_approx(1e23 + 1213141353), '100s')

    def test_precision(self):

        result = num_approx(0, precision=0)
        expected = '0'
        self.assertEqual(result, expected)

        result = num_approx(0, precision=1)
        expected = '0'
        self.assertEqual(result, expected)

        result = num_approx(0, precision=2)
        expected = '0'
        self.assertEqual(result, expected)

        result = num_approx(1.25, precision=0)
        expected = '1'
        self.assertEqual(result, expected)

        result = num_approx(1.85, precision=0)
        expected = '2'
        self.assertEqual(result, expected)

        result = num_approx(1.25, precision=1)
        expected = '1.2'
        self.assertEqual(result, expected)

        result = num_approx(1.25, precision=2)
        expected = '1.25'
        self.assertEqual(result, expected)

        result = num_approx(1.25, precision=3)
        expected = '1.25'
        self.assertEqual(result, expected)

        result = num_approx(321321123, precision=0)
        expected = '321M'
        self.assertEqual(result, expected)

        result = num_approx(321321123, precision=1)
        expected = '321.3M'
        self.assertEqual(result, expected)

        result = num_approx(321321123, precision=4)
        expected = '321.3211M'
        self.assertEqual(result, expected)

        result = num_approx(321321123, precision=9)
        expected = '321.321123M'
        self.assertEqual(result, expected)

    def test_gap(self):

        result = num_approx(0, gap=0)
        expected = '0'
        self.assertEqual(result, expected)

        result = num_approx(0, gap=1)
        expected = '0'
        self.assertEqual(result, expected)

        result = num_approx(0, gap=7)
        expected = '0'
        self.assertEqual(result, expected)

        result = num_approx(1000, gap=0)
        expected = '1K'
        self.assertEqual(result, expected)

        result = num_approx(1000, gap=1)
        expected = '1 K'
        self.assertEqual(result, expected)

        result = num_approx(1000, gap=3)
        expected = '1   K'
        self.assertEqual(result, expected)


class Test__num_round(unittest.TestCase):

    def test_default(self):

        self.assertEqual(num_round(0), '0')
        self.assertEqual(num_round(-1), '-1')
        self.assertEqual(num_round(1), '1')
        self.assertEqual(num_round(1.3), '1')
        self.assertEqual(num_round(1.7), '2')

        self.assertEqual(num_round(11), '11')
        self.assertEqual(num_round(-11), '11')
        self.assertEqual(num_round(69), '69')
        
        self.assertEqual(num_round(111), '110')
        self.assertEqual(num_round(119), '120')
        self.assertEqual(num_round(733), '730')
        self.assertEqual(num_round(-739), '-740')

        self.assertEqual(num_round(1130), '1,100')
        self.assertEqual(num_round(1180), '1,200')
        
        self.assertEqual(num_round(3_331_324), '3,300,000')
        self.assertEqual(num_round(3_371_324), '3,400,000')

    def test_keep(self):
        self.assertEqual(num_round(123_456_789, 0), '100,000,000')  # Will be clamped
        self.assertEqual(num_round(123_456_789, 1), '100,000,000')
        self.assertEqual(num_round(123_456_789, 2), '120,000,000')
        self.assertEqual(num_round(123_456_789, 3), '123,000,000')
        self.assertEqual(num_round(123_456_789, 4), '123,500,000')
        self.assertEqual(num_round(123_456_789, 5), '123,460,000')

    def test_add_commas(self):
        self.assertEqual(num_round(123_456_789, add_commas=False), '120000000')
        self.assertEqual(num_round(123_456_789, add_commas=True ), '120,000,000')


if __name__ == '__main__':
    unittest.main()