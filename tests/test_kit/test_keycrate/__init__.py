import unittest

import os

from mykit.kit.keycrate import KeyCrate


## test_keycrate dir fullpath
dir = os.path.dirname(os.path.abspath(__file__))


class TestKeyCrate(unittest.TestCase):

    def test_must_a_txt_file(self):

        ## test I: success
        pth = os.path.join(dir, 'normal-syntax.txt')
        kc = KeyCrate(pth)
        self.assertIsInstance(kc, KeyCrate)

        ## test II: not a txt file
        pth = os.path.join(dir, 'foo.json')
        with self.assertRaises(ValueError) as context:
            KeyCrate(pth)
        self.assertIsNotNone(context.exception)  # ensure an exception was raised
        self.assertEqual(str(context.exception), f'KeyCrate file {repr(pth)} should be a .txt file.')

        ## test III: not a txt file
        pth = dir
        with self.assertRaises(ValueError) as context:
            KeyCrate(pth)
        self.assertIsNotNone(context.exception)  # ensure an exception was raised
        self.assertEqual(str(context.exception), f'KeyCrate file {repr(pth)} should be a .txt file.')
    

    def test_the_file_must_exist(self):

        ## test I: success
        pth = os.path.join(dir, 'normal-syntax.txt')
        kc = KeyCrate(pth)
        self.assertIsInstance(kc, KeyCrate)

        ## test II: the file doesn't exist
        pth = os.path.join(dir, 'foo.txt')
        with self.assertRaises(FileNotFoundError) as ctx:
            KeyCrate(pth)
        self.assertIsNotNone(ctx.exception)  # ensure an exception was raised
        self.assertEqual(str(ctx.exception), f'KeyCrate file {repr(pth)} is not found.')


    def test_trying_access_nonexistent_key(self):

        pth = os.path.join(dir, 'normal-syntax.txt')
        with self.assertRaises(AttributeError) as ctx:
            kc = KeyCrate(pth)
            kc.notexist  # will raise an exception
        self.assertIsNotNone(ctx.exception)  # ensure an exception was raised
        self.assertEqual(str(ctx.exception), f'KeyCrate file {repr(pth)} does not have key \'notexist\'.')


    def test_normal_syntax_works_fine(self):
        ## this test also checks if the `export` method works correctly

        pth = os.path.join(dir, 'normal-syntax.txt')
        kc = KeyCrate(pth, key_is_var=True, eval_value=True)
        a = kc.export()
        b = {
            'key1': 1,
            'key2': (1, 2),
            'key3000': [1, 2],
            'key4': {1: {1, 2}}
        }
        self.assertEqual(a, b)


    def test_extreme_syntax_works_fine(self):

        pth = os.path.join(dir, 'extreme-syntax.txt')
        kc = KeyCrate(pth, key_is_var=False, eval_value=False)  # note that key_is_var and eval_value are set to False
        a = kc.export()
        b = {
            ':a': ':b:',
            ' ': ' ',  # space-key and space-value
            'abc': 'xyz',
            'abc2': 'pqr!',
            'abc3-4-': '- 1 3 4',
            'abc4-[1, 2, 3]': '[1, 2, 3]',
            'abc5 with spaces': '-abc xyz 123-',
            '-abcd+': '#-- this is a value, not a comment'
        }
        self.assertEqual(a, b)


    def test_invalid_syntax_that_missing_colon(self):

        pth = os.path.join(dir, 'invalid-syntax-that-missing-colon.txt')
        with self.assertRaises(SyntaxError) as ctx:
            KeyCrate(pth)
        self.assertIsNotNone(ctx.exception)  # ensure an exception was raised
        self.assertEqual(str(ctx.exception), f"KeyCrate file {repr(pth)} has invalid syntax at line 5: 'k v'")


    def test_invalid_syntax_that_missing_key(self):

        pth = os.path.join(dir, 'invalid-syntax-that-missing-key.txt')
        with self.assertRaises(SyntaxError) as ctx:
            KeyCrate(pth)
        self.assertIsNotNone(ctx.exception)  # ensure an exception was raised
        self.assertEqual(str(ctx.exception), f"KeyCrate file {repr(pth)} has invalid syntax at line 2: ': '")


    def test_invalid_syntax_that_missing_value(self):

        pth = os.path.join(dir, 'invalid-syntax-that-missing-value.txt')
        with self.assertRaises(SyntaxError) as ctx:
            KeyCrate(pth)
        self.assertIsNotNone(ctx.exception)  # ensure an exception was raised
        self.assertEqual(str(ctx.exception), f"KeyCrate file {repr(pth)} has invalid syntax at line 2: ' :'")  # key without value


    def test_duplicated_key(self):

        pth = os.path.join(dir, 'duplicated-key.txt')
        with self.assertRaises(ValueError) as ctx:
            KeyCrate(pth)
        self.assertIsNotNone(ctx.exception)  # ensure an exception was raised
        self.assertEqual(str(ctx.exception), f"KeyCrate file {repr(pth)} has a duplicated key 'k1' found at line 2.")


    def test_duplicated_key_2(self):
        ## space-key can only be created once

        pth = os.path.join(dir, 'duplicated-key-2.txt')
        with self.assertRaises(ValueError) as ctx:
            KeyCrate(pth)
        self.assertIsNotNone(ctx.exception)  # ensure an exception was raised
        self.assertEqual(str(ctx.exception), f"KeyCrate file {repr(pth)} has a duplicated key ' ' found at line 4.")


if __name__ == '__main__':
    unittest.main()