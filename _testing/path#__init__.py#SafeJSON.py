"""

Testing suite for the `carbon.path.SafeJSON` function.

"""
import os

from carbon import _TESTING_EMPTY_DIR_PTH, _ensure_empty_dir
from carbon.path import SafeJSON


def main():

    print('INFO: Testing `carbon.path.SafeJSON`...')
    _ensure_empty_dir()

    total_test = 0
    total_pass = 0


    ## <testing `SafeJSON.write`>

    ## Test I (Success)
    total_test += 1
    DUMMY_JSON = os.path.join(_TESTING_EMPTY_DIR_PTH, 'dummy.json')
    DUMMY_OBJ = {
        'x': 10,
        'y': 20
    }
    SafeJSON.write(DUMMY_JSON, DUMMY_OBJ)
    if os.path.isfile(DUMMY_JSON):
        total_pass += 1

    ## Test II (Not a JSON type)
    total_test += 1
    try:
        _pth = os.path.join(_TESTING_EMPTY_DIR_PTH, 'dummy.txt')
        SafeJSON.write(_pth, DUMMY_OBJ)
    except AssertionError:
        total_pass += 1

    ## Test III (The parent dir doesn't exist)
    total_test += 1
    try:
        _pth = os.path.join(_TESTING_EMPTY_DIR_PTH, 'nonexistent', 'dummy.json')
        SafeJSON.write(_pth, DUMMY_OBJ)
    except NotADirectoryError:
        total_pass += 1

    ## Test IV (Trying to rewrite the existing file)
    total_test += 1
    try:
        SafeJSON.write(DUMMY_JSON, DUMMY_OBJ)
    except FileExistsError:
        total_pass += 1

    ## </testing `SafeJSON.write`>


    ## <testing `SafeJSON.read`>

    ## Test I (not a JSON file)
    total_test += 1
    try:
        _pth = os.path.join(_TESTING_EMPTY_DIR_PTH, 'dummy.txt')
        SafeJSON.read(_pth)
    except AssertionError:
        total_pass += 1

    ## Test II (the file does not exist)
    total_test += 1
    try:
        _pth = os.path.join(_TESTING_EMPTY_DIR_PTH, 'dummy2.json')
        SafeJSON.read(_pth)
    except FileNotFoundError:
        total_pass += 1

    ## Test III (Success)
    total_test += 1
    if SafeJSON.read(DUMMY_JSON) == DUMMY_OBJ:
        total_pass += 1

    ## </testing `SafeJSON.read`>


    ## </testing `SafeJSON.rewrite`>

    ## Test I (not a JSON file)
    total_test += 1
    try:
        _pth = os.path.join(_TESTING_EMPTY_DIR_PTH, 'dummy.txt')
        SafeJSON.rewrite(_pth, DUMMY_OBJ)
    except AssertionError:
        total_pass += 1
    
    ## Test II (the file does not exist)
    total_test += 1
    try:
        _pth = os.path.join(_TESTING_EMPTY_DIR_PTH, 'dummy2.json')
        SafeJSON.rewrite(_pth, DUMMY_OBJ)
    except FileNotFoundError:
        total_pass += 1
    
    ## Test III (Success)
    total_test += 1
    SafeJSON.rewrite(DUMMY_JSON, {'a': 1})
    if SafeJSON.read(DUMMY_JSON) == {'a': 1}:
        total_pass += 1

    ## </testing `SafeJSON.rewrite`>


    ## Tear down
    print(f'INFO: Tear down: Deleting {repr(DUMMY_JSON)}...')
    os.remove(DUMMY_JSON)

    print(f'INFO: Testing completed: {total_pass}/{total_test} tests passed.')


if __name__ == '__main__':
    main()