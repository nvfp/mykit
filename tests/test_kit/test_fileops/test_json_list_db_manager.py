import unittest

import os
import tempfile

from mykit.kit.fileops.json_list_db_manager import JsonListDbManager


## Note, these tests mostly focus on integration testing, not the unit testing of its dependencies.


class Test__JsonListDbManager(unittest.TestCase):

    def test_core_I(self):  # Empty dir
        
        dir = tempfile.mkdtemp()
        
        self.assertEqual(len(os.listdir(dir)), 0)  # Initially empty
        
        db = JsonListDbManager(dir)
        db.save(0)
        
        self.assertEqual(len(os.listdir(dir)), 1)  # Created new database file

        ## Check the database file
        with open(os.path.join(dir, os.listdir(dir)[0]), 'r') as f:
            self.assertEqual(f.read(), '[0]')

    def test_core_II(self):

        ## Test `max`
        MAX = 3
        
        dir = tempfile.mkdtemp()
        
        db = JsonListDbManager(dir)
        db.bulk_save([1, 2, 3], max=MAX)
        
        self.assertEqual(len(os.listdir(dir)), 1)  # Created new database file
        with open(os.path.join(dir, os.listdir(dir)[0]), 'r') as f: self.assertEqual(f.read(), '[1, 2, 3]')  # Check the database file

        db.save(4, max=MAX)

        self.assertEqual(len(os.listdir(dir)), 2)  # Created new database file
        with open(os.path.join(dir, sorted(os.listdir(dir))[0] ), 'r') as f: self.assertEqual(f.read(), '[1, 2, 3]')  # Check the old database file
        with open(os.path.join(dir, sorted(os.listdir(dir))[-1]), 'r') as f: self.assertEqual(f.read(), '[4]')        # Check the new database file

    def test_core_III(self):

        dir = tempfile.mkdtemp()
        
        db = JsonListDbManager(dir)
        MAX = 3
        db.bulk_save([1, 2, 3, 4, 5, 6, 7], max=MAX)

        self.assertEqual(len(os.listdir(dir)), 3)

        ## Test num_blocks

        self.assertEqual(db.num_blocks, 3)

        ## Test get_partial
        
        result = db.get_partial(0)
        self.assertEqual(result, [1, 2, 3])
        
        result = db.get_partial(1)
        self.assertEqual(result, [4, 5, 6])
        
        result = db.get_partial(2)
        self.assertEqual(result, [7])

        with self.assertRaises(ValueError) as ctx: db.get_partial(-1)
        self.assertEqual(str(ctx.exception), 'Value `idx` out of range.')

        with self.assertRaises(ValueError) as ctx: db.get_partial(3)
        self.assertEqual(str(ctx.exception), 'Value `idx` out of range.')

        ## Test get_all

        result = db.get_all()
        self.assertEqual(result, [1, 2, 3, 4, 5, 6, 7])
    
    def test_validation(self):
        
        ## not a dir
        with self.assertRaises(NotADirectoryError) as ctx: JsonListDbManager('foo')
        self.assertEqual(str(ctx.exception), "Not a dir: 'foo'.")
        
        ## files in dir not valid
        dir = tempfile.mkdtemp()
        open(os.path.join(dir, 'foo.json'), 'w').close()
        open(os.path.join(dir, 'foo.txt'), 'w').close()
        with self.assertRaises(AssertionError) as ctx: JsonListDbManager(dir)
        self.assertEqual(str(ctx.exception), f'All items in {repr(dir)} must be JSON files.')

        ## files in dir not valid II
        dir = tempfile.mkdtemp()
        open(os.path.join(dir, 'foo.json'), 'w').close()
        os.mkdir(os.path.join(dir, 'subdir'))
        with self.assertRaises(AssertionError) as ctx: JsonListDbManager(dir)
        self.assertTrue(
            str(ctx.exception) == f'All items in {repr(dir)} must be JSON files.' or
            str(ctx.exception) == f'Not a file: {repr(dir)}.'
        )


if __name__ == '__main__':
    unittest.main()