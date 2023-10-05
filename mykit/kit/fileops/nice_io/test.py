import TurboTest as tt
from . import NiceIO

import os
import tempfile


## dev-docs: These are the wrong ways to do the tests since the test data
#            can't be shared because the temp file will exist after just one test.
## <delete this soon>

# ## Temporary dir
# TD = tempfile.mkdtemp()


# def read_successfully_empty_file():
    
#     pth = os.path.join(TD, 'test_file.txt')
#     tt.this_is_False(os.path.isfile(pth))
#     open(pth, 'w').close()
#     tt.this_is_True(os.path.isfile(pth))

#     x = NiceIO.read(pth)
#     tt.both_are_equal(x, '')

# def read_successfully_a_file():
    
#     pth = os.path.join(TD, 'test_file.txt')
#     tt.this_is_False(os.path.isfile(pth))
#     with open(pth, 'w') as f: f.write('abc')
#     tt.this_is_True(os.path.isfile(pth))

#     x = NiceIO.read(pth)
#     tt.both_are_equal(x, 'abc')

# def fail_when_reading_nonexistent_file():
#     pth = os.path.join(TD, 'test_file.txt')
#     with tt.these_will_raise(FileNotFoundError) as its: NiceIO.read()

## </delete this soon>


def read_successfully_empty_file():

    temp_dir = tempfile.mkdtemp()
    pth = os.path.join(temp_dir, 'test_file.txt')
    tt.this_is_False(os.path.isfile(pth))
    open(pth, 'w').close()
    tt.this_is_True(os.path.isfile(pth))

    x = NiceIO.read(pth)
    tt.both_are_equal(x, '')

def read_successfully_a_file():
    
    temp_dir = tempfile.mkdtemp()
    pth = os.path.join(temp_dir, 'test_file.txt')
    tt.this_is_False(os.path.isfile(pth))
    with open(pth, 'w') as f: f.write('abc')
    tt.this_is_True(os.path.isfile(pth))

    x = NiceIO.read(pth)
    tt.both_are_equal(x, 'abc')

def fail_when_reading_nonexistent_file():
    temp_dir = tempfile.mkdtemp()
    pth = os.path.join(temp_dir, 'test_file.txt')
    with tt.these_will_raise(FileNotFoundError) as its: NiceIO.read(pth)
    tt.both_are_equal(its.exception_msg, f"Not a file: {repr(pth)}.")

def fail_if_reading_from_an_unexpected_file_type():
    temp_dir = tempfile.mkdtemp()
    pth = os.path.join(temp_dir, 'test_file.txt')
    suffixes = '.py'
    open(pth, 'w').close()  # create the file
    with tt.these_will_raise(AssertionError) as its: NiceIO.read(pth, suffixes)
    tt.both_are_equal(its.exception_msg, f"Invalid suffixes: [expected: {repr(suffixes)}] [got: {repr(pth)}]")



def write_successfully_empty_file():

    temp_dir = tempfile.mkdtemp()
    pth = os.path.join(temp_dir, 'foo.md')
    tt.this_is_False(os.path.isfile(pth))
    NiceIO.write(pth, '')
    tt.this_is_True(os.path.isfile(pth))

    x = NiceIO.read(pth)
    tt.both_are_equal(x, '')

def write_successfully_a_file():

    temp_dir = tempfile.mkdtemp()
    pth = os.path.join(temp_dir, 'foo.md')
    tt.this_is_False(os.path.isfile(pth))
    NiceIO.write(pth, 'hi\nmom')
    tt.this_is_True(os.path.isfile(pth))

    x = NiceIO.read(pth)
    tt.both_are_equal(x, 'hi\nmom')

def fail_to_write_if_unexpected_file_type():
    temp_dir = tempfile.mkdtemp()
    pth = os.path.join(temp_dir, 'foo.md')
    suffixes = '.txt'
    with tt.these_will_raise(AssertionError) as its: NiceIO.write(pth, 'abc', suffixes)
    tt.both_are_equal(its.exception_msg, f"Invalid suffixes: [expected: {repr(suffixes)}] [got: {repr(pth)}]")

def fail_to_write_when_the_parent_dir_does_not_exist():
    temp_dir = tempfile.mkdtemp()
    parent_dir = os.path.join(temp_dir, 'nonexistent')
    pth = os.path.join(parent_dir, 'foo.md')
    with tt.these_will_raise(NotADirectoryError) as its: NiceIO.write(pth, 'abc')
    tt.both_are_equal(its.exception_msg, f"Not a dir: {repr(parent_dir)}.")

def fail_to_write_when_the_target_path_already_exists():
    
    temp_dir = tempfile.mkdtemp()
    pth = os.path.join(temp_dir, 'foo.md')
    
    tt.this_is_False(os.path.isfile(pth))
    open(pth, 'w').close()
    tt.this_is_True(os.path.isfile(pth))

    with tt.these_will_raise(AssertionError) as its: NiceIO.write(pth, '')
    tt.both_are_equal(its.exception_msg, f"Already exists: {repr(pth)}.")



def rewrite_successfully():

    temp_dir = tempfile.mkdtemp()
    pth = os.path.join(temp_dir, 'a.txt')

    tt.this_is_False(os.path.isfile(pth))
    open(pth, 'w').close()
    tt.this_is_True(os.path.isfile(pth))
    tt.both_are_equal(NiceIO.read(pth), '')

    NiceIO.rewrite(pth, 'foo bar\nbaz')
    tt.both_are_equal(NiceIO.read(pth), 'foo bar\nbaz')

def rewrite_successfully_II():

    temp_dir = tempfile.mkdtemp()
    pth = os.path.join(temp_dir, 'a.txt')

    tt.this_is_False(os.path.isfile(pth))
    with open(pth, 'w') as f: f.write('before')
    tt.this_is_True(os.path.isfile(pth))
    tt.both_are_equal(NiceIO.read(pth), 'before')

    NiceIO.rewrite(pth, 'after')
    tt.both_are_equal(NiceIO.read(pth), 'after')

def cant_rewrite_if_unexpected_file_type():
    
    temp_dir = tempfile.mkdtemp()
    pth = os.path.join(temp_dir, 'a.txt')
    suffixes = '.c'

    tt.this_is_False(os.path.isfile(pth))
    with open(pth, 'w') as f: f.write('before')
    tt.this_is_True(os.path.isfile(pth))
    tt.both_are_equal(NiceIO.read(pth), 'before')

    with tt.these_will_raise(AssertionError) as its: NiceIO.rewrite(pth, 'after', suffixes)
    tt.both_are_equal(its.exception_msg, f"Invalid suffixes: [expected: {repr(suffixes)}] [got: {repr(pth)}]")

def cant_rewrite_if_the_file_doesnt_exist():

    temp_dir = tempfile.mkdtemp()
    pth = os.path.join(temp_dir, 'a.txt')

    tt.this_is_True(not os.path.isfile(pth))

    with tt.these_will_raise(FileNotFoundError) as its: NiceIO.rewrite(pth, '')
    tt.both_are_equal(its.exception_msg, f"Not a file: {repr(pth)}.")

def cant_rewrite_when_previous_rewrite_failed():

    temp_dir = tempfile.mkdtemp()

    ## If failed, so .tmp exists
    ## vvvvvvvvvvvvvvvvvvvvvvvvv

    pth = os.path.join(temp_dir, 'a.txt')
    pth_tmp = pth + '.tmp'
    open(pth, 'w').close()
    open(pth_tmp, 'w').close()
    tt.this_is_True(os.path.isfile(pth))
    tt.this_is_True(os.path.isfile(pth_tmp))
    with tt.these_will_raise(AssertionError) as its: NiceIO.rewrite(pth, '')
    tt.both_are_equal(its.exception_msg, f"Already exists: {repr(pth_tmp)}.")

    ## If failed, so .bak exists
    ## vvvvvvvvvvvvvvvvvvvvvvvvv

    pth = os.path.join(temp_dir, 'b.txt')
    pth_bak = pth + '.bak'
    open(pth, 'w').close()
    open(pth_bak, 'w').close()
    tt.this_is_True(os.path.isfile(pth))
    tt.this_is_True(os.path.isfile(pth_bak))
    with tt.these_will_raise(AssertionError) as its: NiceIO.rewrite(pth, '')
    tt.both_are_equal(its.exception_msg, f"Already exists: {repr(pth_bak)}.")



## TODO: write the test suite for `recover` after it's fully developed
# def recover_



def erase_an_existing_file():

    temp_dir = tempfile.mkdtemp()
    pth = os.path.join(temp_dir, 'my.txt')
    with open(pth, 'w') as f: f.write('hi mom\n123')
    tt.both_are_equal(NiceIO.read(pth), 'hi mom\n123')

    NiceIO.erase(pth)
    tt.both_are_equal(NiceIO.read(pth), '')

## These are good to do but not necessary since the above cases
## already cover them (jk, i'm just too lazy to write these out >:D)
# def cant_erase_if_unexpected_file_type(): ...
# def cant_erase_if_the_file_doesnt_exist(): ...
# def cant_erase_when_previous_rewrite_operation_failed(): ...
