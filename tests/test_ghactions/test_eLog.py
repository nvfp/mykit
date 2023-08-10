import unittest

from mykit.ghactions.eLog import eL
from mykit.kit.stream_capture import StreamCapture


class Test__eL(unittest.TestCase):

    def setUp(self):
        eL._testing = True

    def test_set_level(self):
        
        ## Passes

        eL.set_level('quiet')
        eL.set_level('error')
        eL.set_level('Warning')
        eL.set_level('INFO')
        eL.set_level('debuG')

        ## Fails

        with self.assertRaises(ValueError) as ctx: eL.set_level('')
        self.assertEqual(str(ctx.exception), "Invalid level value: ''.")

        with self.assertRaises(ValueError) as ctx: eL.set_level('foo')
        self.assertEqual(str(ctx.exception), "Invalid level value: 'foo'.")

        with self.assertRaises(ValueError) as ctx: eL.set_level(0)
        self.assertEqual(str(ctx.exception), "Invalid level value: 0.")

    def test_default(self):

        with StreamCapture() as captured:
            eL.group('group')
            eL.endgroup('endgroup')
            eL.debug('debug')
            eL.info('info')
            eL.warning('warning')
            eL.error('error')
        result = captured.value
        expected = None
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()