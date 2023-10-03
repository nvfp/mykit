import unittest

import os
import random
import tempfile
import shutil

from mykit.kit.fileops.simple import (
    same_ext_for_all_dir_files, list_dir, remove_all_specific_files_in, definitely_a_dir,
    dont_worry_the_path_ends_with,
    definitely_a_file,
    this_path_must_not_exist,
)


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

        with self.assertRaises(AssertionError) as ctx: same_ext_for_all_dir_files(dir, '.py')
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


class Test__remove_all_specific_files_in(unittest.TestCase):

    def setUp(self):
        self.dir = tempfile.mkdtemp()

        ## Dummy file

        open(os.path.join(self.dir, 'foo.txt'), 'w').close()
        open(os.path.join(self.dir, 'bar.txt'), 'w').close()
        open(os.path.join(self.dir, 'baz.txt'), 'w').close()

        open(os.path.join(self.dir, 'abc.py'), 'w').close()
        open(os.path.join(self.dir, 'xyz.py'), 'w').close()

        ## Subdir

        os.mkdir(os.path.join(self.dir, 'subdir'))
        open(os.path.join(self.dir, 'subdir', 'test1.txt'), 'w').close()
        open(os.path.join(self.dir, 'subdir', 'test2.txt'), 'w').close()
        open(os.path.join(self.dir, 'subdir', 'foobar.js'), 'w').close()

        ## Deeper subdir

        os.mkdir(os.path.join(self.dir, 'subdir', 'subdir2'))
        open(os.path.join(self.dir, 'subdir', 'subdir2', 'f1.txt'), 'w').close()
        open(os.path.join(self.dir, 'subdir', 'subdir2', 'f2.txt'), 'w').close()
        open(os.path.join(self.dir, 'subdir', 'subdir2', 'b.ts'), 'w').close()

        ## Validate

        self.assertEqual(sorted(os.listdir(self.dir)), ['abc.py', 'bar.txt', 'baz.txt', 'foo.txt', 'subdir', 'xyz.py'])
        self.assertEqual(sorted(os.listdir(os.path.join(self.dir, 'subdir'))), ['foobar.js', 'subdir2', 'test1.txt', 'test2.txt'])
        self.assertEqual(sorted(os.listdir(os.path.join(self.dir, 'subdir', 'subdir2'))), ['b.ts', 'f1.txt', 'f2.txt'])

    def tearDown(self):
        shutil.rmtree(self.dir)

    def test_delete_every_file(self):
        deleted = remove_all_specific_files_in(self.dir, r'.*', True)
        self.assertEqual(sorted(deleted), [
            os.path.join(self.dir, 'abc.py'),
            os.path.join(self.dir, 'bar.txt'),
            os.path.join(self.dir, 'baz.txt'),
            os.path.join(self.dir, 'foo.txt'),
            os.path.join(self.dir, 'subdir', 'foobar.js'),
            os.path.join(self.dir, 'subdir', 'subdir2', 'b.ts'),
            os.path.join(self.dir, 'subdir', 'subdir2', 'f1.txt'),
            os.path.join(self.dir, 'subdir', 'subdir2', 'f2.txt'),
            os.path.join(self.dir, 'subdir', 'test1.txt'),
            os.path.join(self.dir, 'subdir', 'test2.txt'),
            os.path.join(self.dir, 'xyz.py'),
        ])
        self.assertEqual(sorted(os.listdir(self.dir)), ['subdir'])
        self.assertEqual(sorted(os.listdir(os.path.join(self.dir, 'subdir'))), ['subdir2'])
        self.assertEqual(sorted(os.listdir(os.path.join(self.dir, 'subdir', 'subdir2'))), [])

    def test_delete_based_on_extension(self):
        remove_all_specific_files_in(self.dir, r'.*?\.txt$', True)
        self.assertEqual(sorted(os.listdir(self.dir)), ['abc.py', 'subdir', 'xyz.py'])
        self.assertEqual(sorted(os.listdir(os.path.join(self.dir, 'subdir'))), ['foobar.js', 'subdir2'])
        self.assertEqual(sorted(os.listdir(os.path.join(self.dir, 'subdir', 'subdir2'))), ['b.ts'])

    def test_delete_based_on_prefix(self):
        remove_all_specific_files_in(self.dir, r'^f.*', True)
        self.assertEqual(sorted(os.listdir(self.dir)), ['abc.py', 'bar.txt', 'baz.txt', 'subdir', 'xyz.py'])
        self.assertEqual(sorted(os.listdir(os.path.join(self.dir, 'subdir'))), ['subdir2', 'test1.txt', 'test2.txt'])
        self.assertEqual(sorted(os.listdir(os.path.join(self.dir, 'subdir', 'subdir2'))), ['b.ts'])

    def test_delete_no_match(self):
        remove_all_specific_files_in(self.dir, r'999', True)
        self.assertEqual(sorted(os.listdir(self.dir)), ['abc.py', 'bar.txt', 'baz.txt', 'foo.txt', 'subdir', 'xyz.py'])
        self.assertEqual(sorted(os.listdir(os.path.join(self.dir, 'subdir'))), ['foobar.js', 'subdir2', 'test1.txt', 'test2.txt'])
        self.assertEqual(sorted(os.listdir(os.path.join(self.dir, 'subdir', 'subdir2'))), ['b.ts', 'f1.txt', 'f2.txt'])

    def test_delete_no_recursive(self):
        deleted = remove_all_specific_files_in(self.dir, r'.*?\.py$', False)
        self.assertEqual(sorted(deleted), [
            os.path.join(self.dir, 'abc.py'),
            os.path.join(self.dir, 'xyz.py'),
        ])
        self.assertEqual(sorted(os.listdir(self.dir)), ['bar.txt', 'baz.txt', 'foo.txt', 'subdir'])
        self.assertEqual(sorted(os.listdir(os.path.join(self.dir, 'subdir'))), ['foobar.js', 'subdir2', 'test1.txt', 'test2.txt'])
        self.assertEqual(sorted(os.listdir(os.path.join(self.dir, 'subdir', 'subdir2'))), ['b.ts', 'f1.txt', 'f2.txt'])


class Test__definitely_a_dir(unittest.TestCase):

    def test(self):

        ## Pass

        p = tempfile.mkdtemp()
        pth = os.path.join(p, 'test_dir')
        os.mkdir(pth)
        definitely_a_dir(pth)

        ## Fail

        pth = os.path.join(p, 'test_dir2')
        with self.assertRaises(NotADirectoryError) as ctx: definitely_a_dir(pth)
        self.assertEqual(str(ctx.exception), f"Not a dir: {repr(pth)}.")


class Test__dont_worry_the_path_ends_with(unittest.TestCase):

    def test_empty_string_suffixes(self):
        with self.assertRaises(ValueError) as ctx: dont_worry_the_path_ends_with('/path/foo', '')
        self.assertEqual(str(ctx.exception), "`suffixes` shouldn't be an empty string.")

    def test_core(self):
        
        dont_worry_the_path_ends_with('init_log.txt', '_log.txt')

        with self.assertRaises(AssertionError) as ctx: dont_worry_the_path_ends_with('testfile.txt', '_log.txt')
        self.assertEqual(str(ctx.exception), "Invalid suffixes: [expected: '_log.txt'] [got: 'testfile.txt']")

        dont_worry_the_path_ends_with('file.txt', ('.txt', '.log'))
        dont_worry_the_path_ends_with('file.log', ('.txt', '.log'))

        with self.assertRaises(AssertionError) as ctx: dont_worry_the_path_ends_with('file.cpp', ('.txt', '.log'))
        self.assertEqual(str(ctx.exception), "Invalid suffixes: [expected: ('.txt', '.log')] [got: 'file.cpp']")
        
        dont_worry_the_path_ends_with('x.foo', ['.FOO', '.BAR'])
        dont_worry_the_path_ends_with('x.FOO', ['.foo', '.bar'])
        dont_worry_the_path_ends_with('x.Foo', '.foo', True)

        with self.assertRaises(AssertionError) as ctx: dont_worry_the_path_ends_with('x.Foo', '.foo', False)
        self.assertEqual(str(ctx.exception), "Invalid suffixes: [expected: '.foo'] [got: 'x.Foo']")


class Test__definitely_a_file(unittest.TestCase):

    def test(self):
        
        p = tempfile.mkdtemp()
        
        ## Pass

        pth = os.path.join(p, 'test_file.txt')
        open(pth, 'w').close()
        definitely_a_file(pth)

        ## Fail

        pth = os.path.join(p, 'test_file2.txt')
        with self.assertRaises(FileNotFoundError) as ctx: definitely_a_file(pth)
        self.assertEqual(str(ctx.exception), f"Not a file: {repr(pth)}.")


class Test__this_path_must_not_exist(unittest.TestCase):

    def test(self):
        
        p = tempfile.mkdtemp()
        

        ## Pass
        ## vvvv

        ## file
        pth = os.path.join(p, 'test_file.txt')
        self.assertEqual(os.path.isfile(pth), False)
        this_path_must_not_exist(pth)

        ## dir
        pth = os.path.join(p, 'test_dir.txt')
        self.assertEqual(os.path.isdir(pth), False)
        this_path_must_not_exist(pth)


        ## Fail
        ## vvvv

        ## file
        pth = os.path.join(p, 'test_file2.txt')
        open(pth, 'w').close()
        self.assertEqual(os.path.isfile(pth), True)
        with self.assertRaises(AssertionError) as ctx: this_path_must_not_exist(pth)
        self.assertEqual(str(ctx.exception), f"Already exists: {repr(pth)}.")

        ## dir
        pth = os.path.join(p, 'test_dir2.txt')
        os.mkdir(pth)
        self.assertEqual(os.path.isdir(pth), True)
        with self.assertRaises(AssertionError) as ctx: this_path_must_not_exist(pth)
        self.assertEqual(str(ctx.exception), f"Already exists: {repr(pth)}.")


if __name__ == '__main__':
    unittest.main()
