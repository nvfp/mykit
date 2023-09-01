import unittest  # The testing framework

## The ones being tested
from mykit.kit.shell import (
    run
)

## Additional helper modules
import os
import tempfile


class Test__run(unittest.TestCase):

    def test(self):
        cwd = tempfile.mkdtemp()
        self.assertEqual(os.listdir(cwd), [])
        run('git init --quiet', cwd=cwd)
        self.assertEqual(os.listdir(cwd), ['.git'])
        run('mkdir foo', cwd=cwd)
        self.assertEqual(sorted(os.listdir(cwd)), ['.git', 'foo'])


if __name__ == '__main__':
    unittest.main()