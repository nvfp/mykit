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


if __name__ == '__main__':
    unittest.main()