import unittest

import subprocess as sp

from mykit.kit.stream_capture import StreamCapture


class Test__StreamCapture(unittest.TestCase):

    def test(self):

        with StreamCapture() as captured:
            pass
        result = captured.value
        expected = ''
        self.assertEqual(result, expected)

        with StreamCapture() as captured:
            print(123)
        result = captured.value
        expected = '132'
        self.assertEqual(result, expected)

        with StreamCapture() as captured:
            print('foo\n\nbar')
            print('baz')
        result = captured.value
        expected = 'foo\n\nbar\nbaz\n'
        self.assertEqual(result, expected)

        with StreamCapture() as captured:
            sp.run(['echo', 'foo'])
        result = captured.value
        expected = 'foo'
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()