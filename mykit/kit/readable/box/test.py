import unittest

from mykit.kit.readable.box import box

from mykit.kit.color import Colored, Hex


class Test__box(unittest.TestCase):

    def test_single(self):
        
        text = 'hi 123'
        result = box(text)
        expected = (
            '==========\n'
            '||hi 123||\n'
            '=========='
        )
        self.assertEqual(result, expected)

    def test_multi(self):
        
        text = (
            '  123 456\n'
            '  foo bar baz\n'
            '  foo bar baz xyz  \n'
            '\n'
            '  foo'
            '\n'
        )
        result = box(text)
        expected = (
            '=======================\n'
            '||  123 456          ||\n'
            '||  foo bar baz      ||\n'
            '||  foo bar baz xyz  ||\n'
            '||                   ||\n'
            '||  foo              ||\n'
            '||                   ||\n'
            '======================='
        )
        self.assertEqual(result, expected)

    ## dev-docs: Since the `box` dependency `_paragraph_width` has already been tested to handle `Colored` text, the test below is not needed.
    # def test_colored_text(self):
    #     pass


if __name__ == '__main__':
    unittest.main()
