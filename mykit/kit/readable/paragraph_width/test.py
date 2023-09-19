import unittest

from mykit.kit.readable.paragraph_width import paragraph_width

from mykit.kit.color import Colored, Hex


class Test__paragraph_width(unittest.TestCase):

    def test_plain_text_single(self):
        
        text = ''
        result = paragraph_width(text)
        self.assertEqual(result, 0)
        
        text = 'hi'
        result = paragraph_width(text)
        self.assertEqual(result, 2)

    def test_plain_text_multi(self):
        
        text = 'hi\n123'
        result = paragraph_width(text)
        self.assertEqual(result, 3)
        
        text = (
            '123\n'
            '12345\n'
            '12\n'
            '1234567\n'
            '123'
        )
        result = paragraph_width(text)
        self.assertEqual(result, 7)

    def test_colored_text_single(self):
        
        text = Colored('hi')
        result = paragraph_width(text)
        self.assertEqual(result, 2)

    def test_colored_text_multi(self):
        
        text = (
            "12\n"
            f"{Colored('123', Hex.RED, Hex.BLACK)}\n"
            "1234\n"
            f"{Colored('12345')}\n"
            "1"
        )
        result = paragraph_width(text)
        self.assertEqual(result, 5)


if __name__ == '__main__':
    unittest.main()
