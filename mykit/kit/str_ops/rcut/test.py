import TurboTest as tt
from . import rcut


def Normal():

    tt.both_are_equal(rcut('foo12', '12'), 'foo')
    tt.both_are_equal(rcut('hi mom 123', ' 123'), 'hi mom')
    tt.both_are_equal(rcut('hi mom', 'cool'), 'hi mom')

    tt.both_are_equal(rcut('', 'ok'), '')
    tt.both_are_equal(rcut('abc', 'abc'), '')
    
    tt.both_are_equal(rcut('abc ', ' '), 'abc')
    
    tt.both_are_equal(rcut('abc', '123'), 'abc')
    tt.both_are_equal(rcut('oh my god', 'oh'), 'oh my god')

    ## Escaped chars
    tt.both_are_equal(rcut('a\nb', 'b'), 'a\n')
    tt.both_are_equal(rcut('a\nb', '\nb'), 'a')


def reject_empty_unwanted_arg():
    with tt.these_will_raise(ValueError) as its: rcut('hi', '')
    tt.both_are_equal(its.exception_msg, "rcut: `unwanted` shouldn't be an empty string.")


def Test_check():

    ## When False
    tt.both_are_equal(rcut('oh my god', '123'), 'oh my god')

    ## When True
    with tt.these_will_raise(AssertionError) as its: rcut('oh my god', '123', check=True)
    tt.both_are_equal(its.exception_msg, "rcut: the given `input_str` does not end with `unwanted`.")
