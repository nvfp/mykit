import unittest

import json
import os
import time

from mykit.kit.path import SafeJSON


class TestSafeJSON(unittest.TestCase):

    def setUp(self) -> None:
        
        ## the directory path containing this test file
        pth = os.path.dirname(__file__)

        ## the directory for holding the dummy files for testing
        pth2 = os.path.join(pth, f'test_path_{round(time.time())}')
        
        ## extra check
        if os.path.exists(pth2):
            raise AssertionError(f'Directory already exists: {repr(pth2)}.')
        
        ## create the dir
        os.mkdir(pth2)
        self.dummy_dir = pth2
    
    def tearDown(self) -> None:

        # print('DEBUG: Removing in 2 secs...')
        # time.sleep(2)
        
        for file in os.listdir(self.dummy_dir):
            
            file_pth = os.path.join(self.dummy_dir, file)
            os.remove(file_pth)
            # print(f'INFO: Deleted: {repr(file_pth)}.')
        
        os.rmdir(self.dummy_dir)
        # print(f'INFO: Deleted: {repr(self.dummy_dir)}.')

    ## SafeJSON.write

    def test_write_valid_json(self):

        ## test writing a valid JSON file
        path = os.path.join(self.dummy_dir, 'test.json')
        obj = {'key': 'value'}
        SafeJSON.write(path, obj, do_log=False)
        
        ## assert that the file exists
        self.assertTrue(os.path.exists(path))
        
        ## assert that the file contains the correct JSON content
        with open(path, 'r') as fp:
            data = json.load(fp)
        self.assertEqual(data, obj)

    def test_write_invalid_extension(self):

        ## test writing a file with an invalid extension
        path = os.path.join(self.dummy_dir, 'test.txt')
        obj = {'key': 'value'}
        
        ## assert that an AssertionError is raised
        with self.assertRaises(AssertionError):
            SafeJSON.write(path, obj)

    def test_write_nonexistent_directory(self):
        
        ## test writing to a nonexistent directory
        path = os.path.join(self.dummy_dir, 'nonexistent_dir', 'test.json')
        obj = {'key': 'value'}
        
        ## assert that a NotADirectoryError is raised
        with self.assertRaises(NotADirectoryError):
            SafeJSON.write(path, obj)

    def test_write_existing_file(self):
        
        ## test writing to an existing file
        path = os.path.join(self.dummy_dir, 'existing_file.json')
        obj = {'key': 'value'}

        ## create a file at the path
        with open(path, 'w') as fp:
            fp.write('existing file')

        ## assert that a FileExistsError is raised
        with self.assertRaises(FileExistsError):
            SafeJSON.write(path, obj)


if __name__ == '__main__':
    unittest.main()