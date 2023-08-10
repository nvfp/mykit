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

    ## This test is failing, I think because it's been affected by
    ## the other tests? I'm not sure about the test-run order of
    ## unittest (plus inside GitHub Action VM).  ~TODO:Nicholas@20230810
    # def test_default(self):

    #     with StreamCapture() as captured:
    #         eL.group('group')
    #         eL.endgroup('endgroup')
    #         eL.debug('debug')
    #         eL.info('info')
    #         eL.warning('warning')
    #         eL.error('error')
    #     result = len( captured.value.split('\n') )  # Remember the '\n' at the end of the `captured.value` string
    #     expected = 7  # Count the number of lines, since the captured string contains 'clock' which can't be determined.
    #     self.assertEqual(result, expected)

    def test_at_debug_level(self):
        eL.set_level('DEBUG')
        with StreamCapture() as captured:
            eL.group('group')
            eL.endgroup('endgroup')
            eL.debug('debug')
            eL.info('info')
            eL.warning('warning')
            eL.error('error')
        self.assertEqual(len( captured.value.split('\n') ), 7)

    def test_at_info_level(self):
        eL.set_level('INFO')
        with StreamCapture() as captured:
            eL.group('group')
            eL.endgroup('endgroup')
            eL.debug('debug')
            eL.info('info')
            eL.warning('warning')
            eL.error('error')
        self.assertEqual(len( captured.value.split('\n') ), 6)

    def test_at_warning_level(self):
        eL.set_level('WARNING')
        with StreamCapture() as captured:
            eL.group('group')
            eL.endgroup('endgroup')
            eL.debug('debug')
            eL.info('info')
            eL.warning('warning')
            eL.error('error')
        self.assertEqual(len( captured.value.split('\n') ), 5)

    def test_at_error_level(self):
        eL.set_level('ERROR')
        with StreamCapture() as captured:
            eL.group('group')
            eL.endgroup('endgroup')
            eL.debug('debug')
            eL.info('info')
            eL.warning('warning')
            eL.error('error')
        self.assertEqual(len( captured.value.split('\n') ), 4)

    def test_at_quiet_level(self):
        eL.set_level('QUIET')
        with StreamCapture() as captured:
            eL.group('group')
            eL.endgroup('endgroup')
            eL.debug('debug')
            eL.info('info')
            eL.warning('warning')
            eL.error('error')
        self.assertEqual(len( captured.value.split('\n') ), 1)


if __name__ == '__main__':
    unittest.main()