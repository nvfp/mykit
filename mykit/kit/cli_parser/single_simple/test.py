import unittest

from mykit.kit.cli_parser.single_simple import SingleSimple

from mykit.kit.color import Colored, Hex
from mykit.kit.stream_capture import StreamCapture


class Test__SingleSimple(unittest.TestCase):

    def setUp(self):
        self.parser = SingleSimple('foo', '123', 'foo bar baz')
        self.parser.add('c1', lambda:print('c1!'), 'test desc')
        self.parser.add('c2345', lambda:print('c2!'), 'test desc 123')

    def test_help_msg(self):
        
        with StreamCapture() as captured:
            self.parser._run_inner(['...'], True)
        
        result = captured.value
        expected = (
            '\n'
            "================================================\n"
            "||                                            ||\n"
            "|| Commands:                                  ||\n"
          # "||   foo       -> show this message then exit ||\n"
          # "||   foo c1    -> test desc                   ||\n"
          # "||   foo c2345 -> test desc 123               ||\n"
            f"||   {Colored('foo c1', Hex.CORN)}    -> {Colored('test desc', Hex.CORN)}                   ||\n"
            f"||   {Colored('foo c2345', Hex.CORN)} -> {Colored('test desc 123', Hex.CORN)}               ||\n"
            f"||   {Colored('foo', Hex.CORN)}       -> {Colored('show this message then exit', Hex.CORN)} ||\n"
            "||                                            ||\n"
            "|| Info:                                      ||\n"
            "||   software  : foo                          ||\n"
            "||   version   : 123                          ||\n"
            "||   repository: foo bar baz                  ||\n"
            "||                                            ||\n"
            "================================================"
            '\n'  # effect from the `print` function
        )
        self.assertEqual(result, expected)

    def test_invalid_input_command(self):

        with StreamCapture() as captured:
            self.parser._run_inner(['...', 'c3'], True)
        
        result = captured.value
        expected = "Unknown commands 'c3', run `foo` for help.\n"
        self.assertEqual(result, expected)
    
    def test_run_the_functions(self):
        
        with StreamCapture() as captured:
            self.parser._run_inner(['...', 'c1'], True)
        self.assertEqual(captured.value, 'c1!\n')

        with StreamCapture() as captured:
            self.parser._run_inner(['...', 'c2345'], True)
        self.assertEqual(captured.value, 'c2!\n')


if __name__ == '__main__':
    unittest.main()
