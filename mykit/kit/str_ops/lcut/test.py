import TurboTest as tt
from . import lcut


def Normal():
    tt.both_are_equal(lcut('121foo', '12'), '1foo')
    tt.both_are_equal(lcut('123 hi mom 123', '123 '), 'hi mom 123')
    tt.both_are_equal(lcut('hi mom', 'cool'), 'hi mom')

    tt.both_are_equal(lcut('', 'ok'), '')
    tt.both_are_equal(lcut('abc', 'abc'), '')
    
    tt.both_are_equal(lcut(' abc', ' '), 'abc')
    
    tt.both_are_equal(lcut('abc', '123'), 'abc')
    tt.both_are_equal(lcut('oh my god', 'god'), 'oh my god')

    ## Escaped chars
    tt.both_are_equal(lcut('a\nb', 'a'), '\nb')
    tt.both_are_equal(lcut('a\nb', 'a\n'), 'b')


def reject_empty_unwanted_arg():
    with tt.these_will_raise(ValueError) as its: lcut('hi', '')
    tt.both_are_equal(its.exception_msg, "lcut: `unwanted` shouldn't be an empty string.")


def Test_check():

    ## When False
    tt.both_are_equal(lcut('oh my god', '123'), 'oh my god')

    ## When True
    with tt.these_will_raise(AssertionError) as its: lcut('oh my god', '123', check=True)
    tt.both_are_equal(its.exception_msg, "lcut: the given `input_str` does not start with `unwanted`.")
