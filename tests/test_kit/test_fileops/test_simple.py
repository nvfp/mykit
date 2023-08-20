import unittest

import os
import random
import tempfile

from mykit.kit.fileops.simple import same_ext_for_all_dir_files, list_dir


class Test__same_ext_for_all_dir_files(unittest.TestCase):

    def test_core_I(self):  # Empty dir
        dir = tempfile.mkdtemp()
        result = same_ext_for_all_dir_files(dir, '.foo')
        self.assertEqual(result, True)

    def test_core_II(self):  # All files are the same type
        
        dir = tempfile.mkdtemp()
        n = random.randint(1, 10)
        for i in range(n): open(os.path.join(dir, f'file_{i}.TXT'), 'w').close()

        self.assertEqual(len(os.listdir(dir)), n)  # Debugging purposes

        result = same_ext_for_all_dir_files(dir, '.txt')
        self.assertEqual(result, True)

    def test_core_III(self):  # Files are of different types
        
        dir = tempfile.mkdtemp()
        n = random.randint(1, 10)
        for i in range(n): open(os.path.join(dir, f'file_{i}.txT'), 'w').close()
        for i in range(n): open(os.path.join(dir, f'file_{i}.mdx'), 'w').close()

        result = same_ext_for_all_dir_files(dir, '.tXt')
        self.assertEqual(result, False)

    def test_not_a_dir(self):

        ## Test I

        with self.assertRaises(NotADirectoryError) as ctx: same_ext_for_all_dir_files('foo', '.foo')
        self.assertEqual(str(ctx.exception), "Not a dir: 'foo'.")

        ## Test II
        
        dir = tempfile.mkdtemp()
        pth = os.path.join(dir, 'file.txt')
        open(pth, 'w').close()

        self.assertEqual(os.path.isfile(pth), True)  # Debugging purposes
        
        with self.assertRaises(NotADirectoryError) as ctx: same_ext_for_all_dir_files(pth, '.foo')
        self.assertEqual(str(ctx.exception), f'Not a dir: {repr(pth)}.')

    def test_extension_validity(self):

        dir = tempfile.mkdtemp()

        ## Passes

        same_ext_for_all_dir_files(dir, '.foo')
        same_ext_for_all_dir_files(dir, '.123foo')
        same_ext_for_all_dir_files(dir, '.foo_bar_123')

        ## Fails

        with self.assertRaises(ValueError) as ctx: same_ext_for_all_dir_files(dir, '')
        self.assertEqual(str(ctx.exception), "Invalid extension: ''.")

        with self.assertRaises(ValueError) as ctx: same_ext_for_all_dir_files(dir, 'txt')
        self.assertEqual(str(ctx.exception), "Invalid extension: 'txt'.")

        with self.assertRaises(ValueError) as ctx: same_ext_for_all_dir_files(dir, '.txt ')
        self.assertEqual(str(ctx.exception), "Invalid extension: '.txt '.")

        with self.assertRaises(ValueError) as ctx: same_ext_for_all_dir_files(dir, '.txt+')
        self.assertEqual(str(ctx.exception), "Invalid extension: '.txt+'.")
        
    def test_item_is_not_file(self):

        dir = tempfile.mkdtemp()

        ## Dummy data
        for i in range(3): open(os.path.join(dir, f'file_{i}.py'), 'w').close()
        pth = os.path.join(dir, 'subdir')
        os.mkdir(pth)

        with self.assertRaises(FileNotFoundError) as ctx: same_ext_for_all_dir_files(dir, '.py')
        self.assertEqual(str(ctx.exception), f'Not a file: {repr(pth)}.')


class Test__list_dir(unittest.TestCase):

    def test_core_I(self):  # Empty dir
        dir = tempfile.mkdtemp()
        result = list_dir(dir)
        expected = []
        self.assertEqual(result, expected)

    def test_core_II(self):  # normal
        
        dir = tempfile.mkdtemp()
        name = 'file.py'
        pth = os.path.join(dir, name)
        open(pth, 'w').close()

        result = list_dir(dir)
        expected = [(name, pth)]
        self.assertEqual(result, expected)

    def test_core_III(self):  # normal
        
        dir = tempfile.mkdtemp()
        for i in range(3): open(os.path.join(dir, f'file_{i}.txt'), 'w').close()

        result = sorted(list_dir(dir))  # Sorting to double-check expected behavior
        expected = [
            ('file_0.txt', os.path.join(dir, 'file_0.txt')),
            ('file_1.txt', os.path.join(dir, 'file_1.txt')),
            ('file_2.txt', os.path.join(dir, 'file_2.txt')),
        ]
        self.assertEqual(result, expected)

    def test_core_IV(self):  # normal
        
        dir = tempfile.mkdtemp()
        for i in range(3): open(os.path.join(dir, f'file_{i}.txt'), 'w').close()
        for i in range(3): os.mkdir(os.path.join(dir, f'subdir_{i}'))

        self.assertEqual(len(os.listdir(dir)), 6)  # Debugging purposes

        result = sorted(list_dir(dir))  # Sorting to double-check expected behavior
        expected = [
            ('file_0.txt', os.path.join(dir, 'file_0.txt')),
            ('file_1.txt', os.path.join(dir, 'file_1.txt')),
            ('file_2.txt', os.path.join(dir, 'file_2.txt')),
            ('subdir_0', os.path.join(dir, 'subdir_0')),
            ('subdir_1', os.path.join(dir, 'subdir_1')),
            ('subdir_2', os.path.join(dir, 'subdir_2')),
        ]
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()