import os
import sys
import unittest

# Add the parent directory to the sys.path
print(sys.path)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
print(sys.path)

# # Import the modules with modified import statements
# import dir.file
# # Add more import statements as needed

# # Discover and run the tests
# test_loader = unittest.TestLoader()
# test_suite = test_loader.discover("tests", pattern="test_*.py")
# test_runner = unittest.TextTestRunner()
# test_runner.run(test_suite)
