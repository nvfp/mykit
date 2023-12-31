import unittest

import os

from mykit.kit.keycrate import KeyCrate


## test_keycrate dir fullpath
DIR = os.path.dirname(os.path.abspath(__file__))


class TestKeyCrate(unittest.TestCase):

    def test_must_a_txt_file(self):

        ## test I: success
        pth = os.path.join(DIR, 'normal-syntax.txt')
        kc = KeyCrate(pth)
        self.assertIsInstance(kc, KeyCrate)

        ## test II: not a txt file
        pth = os.path.join(DIR, 'foo.json')
        with self.assertRaises(ValueError) as context:
            KeyCrate(pth)
        self.assertIsNotNone(context.exception)  # ensure an exception was raised
        self.assertEqual(str(context.exception), f'KeyCrate file {repr(pth)} should be a .txt file.')

        ## test III: not a txt file
        pth = DIR
        with self.assertRaises(ValueError) as context:
            KeyCrate(pth)
        self.assertIsNotNone(context.exception)  # ensure an exception was raised
        self.assertEqual(str(context.exception), f'KeyCrate file {repr(pth)} should be a .txt file.')
    

    def test_the_file_must_exist(self):

        ## test I: success
        pth = os.path.join(DIR, 'normal-syntax.txt')
        kc = KeyCrate(pth)
        self.assertIsInstance(kc, KeyCrate)

        ## test II: the file doesn't exist
        pth = os.path.join(DIR, 'foo.txt')
        with self.assertRaises(FileNotFoundError) as ctx:
            KeyCrate(pth)
        self.assertIsNotNone(ctx.exception)
        self.assertEqual(str(ctx.exception), f'KeyCrate file {repr(pth)} is not found.')


    def test_trying_access_nonexistent_key(self):

        pth = os.path.join(DIR, 'normal-syntax.txt')
        with self.assertRaises(AttributeError) as ctx:
            kc = KeyCrate(pth)
            kc.notexist  # will raise an exception
        self.assertIsNotNone(ctx.exception)
        self.assertEqual(str(ctx.exception), f'KeyCrate file {repr(pth)} does not have key \'notexist\'.')


    def test_normal_syntax_works_fine(self):
        ## this test also checks if the `export` method works correctly

        pth = os.path.join(DIR, 'normal-syntax.txt')
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

        pth = os.path.join(DIR, 'extreme-syntax.txt')
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

        pth = os.path.join(DIR, 'invalid-syntax-that-missing-colon.txt')
        with self.assertRaises(SyntaxError) as ctx:
            KeyCrate(pth)
        self.assertIsNotNone(ctx.exception)
        self.assertEqual(str(ctx.exception), f"KeyCrate file {repr(pth)} has invalid syntax at line 5: 'k v'")


    def test_invalid_syntax_that_missing_key(self):

        pth = os.path.join(DIR, 'invalid-syntax-that-missing-key.txt')
        with self.assertRaises(SyntaxError) as ctx:
            KeyCrate(pth)
        self.assertIsNotNone(ctx.exception)
        self.assertEqual(str(ctx.exception), f"KeyCrate file {repr(pth)} has invalid syntax at line 2: ': '")


    def test_invalid_syntax_that_missing_value(self):

        pth = os.path.join(DIR, 'invalid-syntax-that-missing-value.txt')
        with self.assertRaises(SyntaxError) as ctx:
            KeyCrate(pth)
        self.assertIsNotNone(ctx.exception)
        self.assertEqual(str(ctx.exception), f"KeyCrate file {repr(pth)} has invalid syntax at line 2: ' :'")  # key without value


    def test_duplicated_key(self):

        pth = os.path.join(DIR, 'duplicated-key.txt')
        with self.assertRaises(ValueError) as ctx:
            KeyCrate(pth)
        self.assertIsNotNone(ctx.exception)
        self.assertEqual(str(ctx.exception), f"KeyCrate file {repr(pth)} has a duplicated key 'k1' found at line 2.")


    def test_duplicated_key_2(self):
        ## space-key can only be created once

        pth = os.path.join(DIR, 'duplicated-key-2.txt')
        with self.assertRaises(ValueError) as ctx:
            KeyCrate(pth)
        self.assertIsNotNone(ctx.exception)
        self.assertEqual(str(ctx.exception), f"KeyCrate file {repr(pth)} has a duplicated key ' ' found at line 4.")


    def test_key_is_var(self):

        ## test I
        pth = os.path.join(DIR, 'key_is_var-fail-1.txt')
        with self.assertRaises(AssertionError) as ctx:
            KeyCrate(pth, key_is_var=True)
        self.assertIsNotNone(ctx.exception)
        self.assertEqual(str(ctx.exception), f"KeyCrate file {repr(pth)} has a key 'k-' that is invalid for a variable name, found at line 1.")

        ## test II
        pth = os.path.join(DIR, 'key_is_var-fail-2.txt')
        with self.assertRaises(AssertionError) as ctx:
            KeyCrate(pth, key_is_var=True)
        self.assertIsNotNone(ctx.exception)
        self.assertEqual(str(ctx.exception), f"KeyCrate file {repr(pth)} has a key '-k' that is invalid for a variable name, found at line 1.")

        ## test III
        pth = os.path.join(DIR, 'key_is_var-fail-3.txt')
        with self.assertRaises(AssertionError) as ctx:
            KeyCrate(pth, key_is_var=True)
        self.assertIsNotNone(ctx.exception)
        self.assertEqual(str(ctx.exception), f"KeyCrate file {repr(pth)} has a key '1k' that is invalid for a variable name, found at line 1.")
    

    def test_eval_value(self):

        ## test I: success
        pth = os.path.join(DIR, 'eval_value-pass.txt')
        kc = KeyCrate(pth, key_is_var=False, eval_value=True)  # NOTE: key_is_var is set to False
        a = kc.export()
        b = {  # reminder: when evaluating, `1 == 1.0` is True
            'a': 'a',
            'b': 'a\nb\nc',
            'c': 1,
            'd': 1.0,
            'e': [1, 2],
            'f': (1, 2),
            'g': {1: 1},
            'h': {1, 2},
            'i': (1, 2),
            'j': [1, 2],
            'k': 9,
            'l': 9
        }
        self.assertEqual(a, b)

        ## test II: users forgot to put quotes around the string, resulting NameError
        pth = os.path.join(DIR, 'eval_value-fail-1.txt')
        with self.assertRaises(AssertionError) as ctx:
            KeyCrate(pth, key_is_var=False, eval_value=True)
        self.assertIsNotNone(ctx.exception)
        self.assertEqual(str(ctx.exception), f"KeyCrate file {repr(pth)} has a value 'b' that cannot be evaluated, found at line 3.")

        ## test III: users forgot to put quotes around the string, resulting SyntaxError
        pth = os.path.join(DIR, 'eval_value-fail-2.txt')
        with self.assertRaises(AssertionError) as ctx:
            KeyCrate(pth, key_is_var=False, eval_value=True)
        self.assertIsNotNone(ctx.exception)
        self.assertEqual(str(ctx.exception), f"KeyCrate file {repr(pth)} has a value 'a b c' that cannot be evaluated, found at line 1.")

        ## test IV: undefined object
        pth = os.path.join(DIR, 'eval_value-fail-3.txt')
        with self.assertRaises(AssertionError) as ctx:
            KeyCrate(pth, key_is_var=False, eval_value=True)
        self.assertIsNotNone(ctx.exception)
        self.assertEqual(str(ctx.exception), f"KeyCrate file {repr(pth)} has a value 'func(0)' that cannot be evaluated, found at line 1.")
    

    def test_only_keys(self):
        
        ## test I: pass
        pth = os.path.join(DIR, 'only_keys-need_keys.txt')
        kc = KeyCrate(pth, only_keys=['k1', 'k2'])
        self.assertIsInstance(kc, KeyCrate)
        
        ## test II: pass: k3 is needed, but it's fine if it doesn't exist
        pth = os.path.join(DIR, 'only_keys-need_keys.txt')
        kc = KeyCrate(pth, only_keys=['k1', 'k2', 'k3'])
        self.assertIsInstance(kc, KeyCrate)

        ## test III: fail: only k1 is allowed in the file
        pth = os.path.join(DIR, 'only_keys-need_keys.txt')
        with self.assertRaises(AssertionError) as ctx:
            KeyCrate(pth, only_keys=['k1'])
        self.assertIsNotNone(ctx.exception)
        self.assertEqual(str(ctx.exception), f"KeyCrate file {repr(pth)} has an unexpected key 'k2' found at line 2.")

        ## test IV: fail: only k3 is allowed in the file
        pth = os.path.join(DIR, 'only_keys-need_keys.txt')
        with self.assertRaises(AssertionError) as ctx:
            KeyCrate(pth, only_keys=['k3'])
        self.assertIsNotNone(ctx.exception)
        self.assertEqual(str(ctx.exception), f"KeyCrate file {repr(pth)} has an unexpected key 'k1' found at line 1.")

    
    def test_need_keys(self):

        ## test I: pass
        pth = os.path.join(DIR, 'only_keys-need_keys.txt')
        kc = KeyCrate(pth, need_keys=['k1', 'k2'])
        self.assertIsInstance(kc, KeyCrate)
        
        ## test II: pass: k2 is optional
        pth = os.path.join(DIR, 'only_keys-need_keys.txt')
        kc = KeyCrate(pth, need_keys=['k1'])
        self.assertIsInstance(kc, KeyCrate)

        ## test III: fail: missing key
        pth = os.path.join(DIR, 'only_keys-need_keys.txt')
        with self.assertRaises(AssertionError) as ctx:
            KeyCrate(pth, need_keys=['k1', 'k2', 'k3'])
        self.assertIsNotNone(ctx.exception)
        self.assertEqual(str(ctx.exception), f"KeyCrate file {repr(pth)} is missing keys: 'k3'")

        ## test IV: fail: only k3 is allowed in the file
        pth = os.path.join(DIR, 'only_keys-need_keys.txt')
        with self.assertRaises(AssertionError) as ctx:
            KeyCrate(pth, need_keys=['k1', 'k2', 'k3', 'k4', 'name, age and job'])
        self.assertIsNotNone(ctx.exception)
        self.assertEqual(str(ctx.exception), f"KeyCrate file {repr(pth)} is missing keys: 'k3', 'k4', 'name, age and job'")


    def test_only_keys_and_need_keys(self):
        
        ## test I: pass
        pth = os.path.join(DIR, 'only_keys-need_keys.txt')
        kc = KeyCrate(pth,
            only_keys=['k1', 'k2'],
            need_keys=['k1', 'k2']
        )
        self.assertIsInstance(kc, KeyCrate)
        
        ## test II: pass
        pth = os.path.join(DIR, 'only_keys-need_keys.txt')
        kc = KeyCrate(pth,
            only_keys=['k1', 'k2', 'k3'],
            need_keys=['k1']
        )
        self.assertIsInstance(kc, KeyCrate)

        ## test III: fail
        pth = os.path.join(DIR, 'only_keys-need_keys.txt')
        with self.assertRaises(AssertionError) as ctx:
            KeyCrate(pth,
                only_keys=['k1', 'k2', 'k3'],
                need_keys=['k1', 'k2', 'k3']
            )
        self.assertIsNotNone(ctx.exception)
        self.assertEqual(str(ctx.exception), f"KeyCrate file {repr(pth)} is missing keys: 'k3'")

        ## test IV: fail
        pth = os.path.join(DIR, 'only_keys-need_keys.txt')
        with self.assertRaises(AssertionError) as ctx:
            KeyCrate(pth,
                only_keys=['k1'],
                need_keys=['k1', 'k2']
            )
        self.assertIsNotNone(ctx.exception)
        self.assertEqual(str(ctx.exception), f"KeyCrate file {repr(pth)} has an unexpected key 'k2' found at line 2.")
    

    def test_only_keys_and_need_keys_as_tuple_of_strings(self):

        ## Test I
        pth = os.path.join(DIR, 'only_keys-need_keys.txt')
        kc = KeyCrate(pth,
            only_keys=('k1', 'k2'),
            need_keys=('k1', 'k2')
        )
        self.assertIsInstance(kc, KeyCrate)

        ## Test II
        def func(*keys):  # `keys` is a tuple of strings
            pth = os.path.join(DIR, 'only_keys-need_keys.txt')
            kc = KeyCrate(pth, only_keys=keys, need_keys=keys)
            self.assertIsInstance(kc, KeyCrate)
        func('k1', 'k2')


if __name__ == '__main__':
    unittest.main()