import unittest

import os
import shutil
import tempfile

from mykit.kit.fileops.equaldirs import equaldirs


class Test__equaldirs(unittest.TestCase):

    def test_not_a_dir(self):
        
        with self.assertRaises(NotADirectoryError) as ctx: equaldirs('foo', 'bar')
        self.assertEqual(str(ctx.exception), "Value `dir1` is not a directory: 'foo'.")

        with self.assertRaises(NotADirectoryError) as ctx: equaldirs(os.path.dirname(__file__), 'bar')
        self.assertEqual(str(ctx.exception), "Value `dir2` is not a directory: 'bar'.")

    def test_both_dirs_empty(self):

        dir1 = tempfile.mkdtemp()
        dir2 = tempfile.mkdtemp()
        
        result = equaldirs(dir1, dir2)
        expected = True
        self.assertEqual(result, expected)

    def test_both_dirs_have_an_identical_single_file(self):

        dir1 = tempfile.mkdtemp()
        dir2 = tempfile.mkdtemp()

        ## Create empty file
        open(os.path.join(dir1, 'file.txt'), 'w').close()
        open(os.path.join(dir2, 'file.txt'), 'w').close()

        result = equaldirs(dir1, dir2)
        expected = True
        self.assertEqual(result, expected)

    def test_both_dirs_have_an_identical_single_file2(self):

        dir1 = tempfile.mkdtemp()
        dir2 = tempfile.mkdtemp()

        with open(os.path.join(dir1, 'file.txt'), 'w') as f: f.write('foo bar')
        with open(os.path.join(dir2, 'file.txt'), 'w') as f: f.write('foo bar')

        result = equaldirs(dir1, dir2)
        expected = True
        self.assertEqual(result, expected)

    def test_both_dirs_equal_1(self):

        dir1 = tempfile.mkdtemp()
        dir2 = tempfile.mkdtemp()

        with open(os.path.join(dir1, 'file.txt'), 'w') as f: f.write('foo bar')
        with open(os.path.join(dir2, 'file.txt'), 'w') as f: f.write('foo bar')

        with open(os.path.join(dir1, 'test.py'), 'w') as f: f.write('123')
        with open(os.path.join(dir2, 'test.py'), 'w') as f: f.write('123')

        os.mkdir(os.path.join(dir1, 'subdir'))
        os.mkdir(os.path.join(dir2, 'subdir'))

        with open(os.path.join(dir1, 'subdir', 'foo.md'), 'w') as f: f.write('abc')
        with open(os.path.join(dir2, 'subdir', 'foo.md'), 'w') as f: f.write('abc')

        self.assertEqual(sorted(os.listdir(dir1)), ['file.txt', 'subdir', 'test.py'])

        result = equaldirs(dir1, dir2)
        expected = True
        self.assertEqual(result, expected)

    def test_both_dirs_equal_2(self):

        dir1 = tempfile.mkdtemp()
        dir2 = tempfile.mkdtemp()

        with open(os.path.join(dir1, 'test_1'), 'w') as f: f.write('abc x')
        with open(os.path.join(dir1, 'test_2'), 'w') as f: f.write('abc y')
        with open(os.path.join(dir1, 'test_3'), 'w') as f: f.write('abc z')

        os.mkdir(os.path.join(dir1, 'subdir_1'))
        os.mkdir(os.path.join(dir1, 'subdir_2'))

        with open(os.path.join(dir1, 'subdir_1', 'abc_1'), 'w') as f: f.write('abc p')
        with open(os.path.join(dir1, 'subdir_2', 'abc_2'), 'w') as f: f.write('abc q')
        
        os.mkdir(os.path.join(dir1, 'subdir_1', 'another_dir'))
        with open(os.path.join(dir1, 'subdir_1', 'another_dir', 'file.js'), 'w') as f: f.write('console.log')
        
        os.makedirs(os.path.join(dir1, 'subdir_2', 'dir_a', 'dir_b', 'dir_c'))
        with open(os.path.join(dir1, 'subdir_2', 'dir_a', 'dir_b', 'dir_c', 'abc.txt'), 'w') as f: f.write('baz')

        self.assertEqual(os.listdir(dir2), [])

        os.rmdir(dir2)  # Needs to be removed for shutil.copytree to work
        shutil.copytree(dir1, dir2)

        self.assertEqual(sorted(os.listdir(dir2)), ['subdir_1', 'subdir_2', 'test_1', 'test_2', 'test_3'])

        result = equaldirs(dir1, dir2)
        expected = True
        self.assertEqual(result, expected)
    
    def test_equal(self):

        dir1 = tempfile.mkdtemp()
        dir2 = tempfile.mkdtemp()

        self.assertEqual(os.listdir(dir1), [])

        os.mkdir(os.path.join(dir1, 'subdir'))
        os.mkdir(os.path.join(dir2, 'subdir'))

        self.assertEqual(os.listdir(dir1), ['subdir'])

        result = equaldirs(dir1, dir2)
        expected = True
        self.assertEqual(result, expected)

    def test_not_equal_1(self):

        dir1 = tempfile.mkdtemp()
        dir2 = tempfile.mkdtemp()

        open(os.path.join(dir1, 'file.txt'), 'w').close()  # Create an empty file

        result = equaldirs(dir1, dir2)
        expected = False
        self.assertEqual(result, expected)

    def test_not_equal_2(self):

        dir1 = tempfile.mkdtemp()
        dir2 = tempfile.mkdtemp()

        os.mkdir(os.path.join(dir2, 'subdir'))  # Create an empty folder

        self.assertEqual(os.listdir(dir1), [])
        self.assertEqual(os.listdir(dir2), ['subdir'])

        result = equaldirs(dir1, dir2)
        expected = False
        self.assertEqual(result, expected)

    def test_not_equal_3(self):

        dir1 = tempfile.mkdtemp()
        dir2 = tempfile.mkdtemp()

        open(os.path.join(dir1, 'file.txt'), 'w').close()  # Create an empty file
        os.mkdir(os.path.join(dir2, 'subdir'))  # Create an empty folder

        self.assertEqual(os.listdir(dir1), ['file.txt'])
        self.assertEqual(os.listdir(dir2), ['subdir'])

        result = equaldirs(dir1, dir2)
        expected = False
        self.assertEqual(result, expected)

    def test_not_equal_4(self):

        dir1 = tempfile.mkdtemp()
        dir2 = tempfile.mkdtemp()

        ## Same file in each dir
        open(os.path.join(dir1, 'file.txt'), 'w').close()
        open(os.path.join(dir2, 'file.txt'), 'w').close()

        with open(os.path.join(dir1, 'foo.txt'), 'w') as f: f.write('foo')
        with open(os.path.join(dir2, 'bar.txt'), 'w') as f: f.write('foo')

        os.mkdir(os.path.join(dir1, 'subdir'))
        os.mkdir(os.path.join(dir2, 'subdir'))

        with open(os.path.join(dir1, 'subdir', 'abcd.txt'), 'w') as f: f.write('foo')
        with open(os.path.join(dir2, 'subdir', 'xyzw.txt'), 'w') as f: f.write('foo')

        os.mkdir(os.path.join(dir1, 'subdir', 'subdir_again'))
        with open(os.path.join(dir1, 'subdir', 'subdir_again', 'foobar.txt'), 'w') as f: f.write('12345')

        os.makedirs(os.path.join(dir2, 'subdir', 'x1', 'x2', 'x3', 'x4'))
        with open(os.path.join(dir2, 'subdir', 'x1', 'x2', 'x3', 'x4', 'pqr.md'), 'w') as f: f.write('abcde')

        result = equaldirs(dir1, dir2)
        expected = False
        self.assertEqual(result, expected)

    def test_not_equal_5(self):

        dir1 = tempfile.mkdtemp()
        dir2 = tempfile.mkdtemp()

        open(os.path.join(dir1, 'foo.txt'), 'w').close()
        open(os.path.join(dir2, 'bar.txt'), 'w').close()

        result = equaldirs(dir1, dir2)
        expected = False
        self.assertEqual(result, expected)

    def test_not_equal_6(self):

        dir1 = tempfile.mkdtemp()
        dir2 = tempfile.mkdtemp()

        os.mkdir(os.path.join(dir1, 'subdir_1'))
        os.mkdir(os.path.join(dir2, 'subdir_2'))

        result = equaldirs(dir1, dir2)
        expected = False
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()