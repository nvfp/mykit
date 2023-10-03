import unittest

from mykit.kit.py_file_compressor import py_file_compressor

import os

# from mykit.kit.


TEST_DATA = os.path.join(os.path.dirname(__file__), 'test_data')


class Test__py_file_compressor(unittest.TestCase):

    def test_set_1(self):

        return

        things = os.listdir(TEST_DATA)
        nThing = len(things)
        nSet = nThing//2  # number of sets

        ## Checks
        if (nThing % 2) != 0: raise AssertionError

        for i in range(nSet):

            pth_original = os.path.join(TEST_DATA, f'set_{i}_original.py')
            pth_compress = os.path.join(TEST_DATA, f'set_{i}_compress.py')
            
            py_file_compressor(pth_before)

            text_result = ''
            text_expected = ''

            self.assertEqual(text_result, text_expected)


if __name__ == '__main__':
    unittest.main()
