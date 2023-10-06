import TurboTest as tt
from . import trim_long_str


def default_value():
    
    x  = 'a'*50
    x += 'b'*25
    x += 'c'*50
    
    result = trim_long_str(x)
    expected = 'a'*50 + '...\n\n   [25 more chars]\n\n...' + 'c'*50
    tt.both_are_equal(result, expected)


def return_the_original_string_if_its_length_is_not_exceeded():

    result = trim_long_str('hi')
    expected = 'hi'
    tt.both_are_equal(result, expected)


def Test_max__char():

    x  = 'a'*5
    x += 'b'*25
    x += 'c'*5    
    result = trim_long_str(x, max_char=10)
    expected = 'a'*5 + '...\n\n   [25 more chars]\n\n...' + 'c'*5
    tt.both_are_equal(result, expected)

    x  = 'a'*10
    x += 'b'*251
    x += 'c'*10
    result = trim_long_str(x, max_char=20)
    expected = 'a'*10 + '...\n\n   [251 more chars]\n\n...' + 'c'*10
    tt.both_are_equal(result, expected)

    x  = 'a'*150
    x += 'b'*1234
    x += 'c'*150
    result = trim_long_str(x, max_char=300)
    expected = 'a'*150 + '...\n\n   [1234 more chars]\n\n...' + 'c'*150
    tt.both_are_equal(result, expected)

    ## odd value max_char
    x  = 'a'*50
    x += 'b'*321
    x += 'c'*50
    result = trim_long_str(x, max_char=101)
    expected = 'a'*50 + '...\n\n   [321 more chars]\n\n...' + 'c'*50
    tt.both_are_equal(result, expected)


def Test_nTab():

    x  = 'a'*50
    x += 'b'*25
    x += 'c'*50
    
    result = trim_long_str(x, nTab=0)
    expected = 'a'*50 + '...\n\n[25 more chars]\n\n...' + 'c'*50
    tt.both_are_equal(result, expected)
    
    result = trim_long_str(x, nTab=2)
    expected = 'a'*50 + '...\n\n  [25 more chars]\n\n...' + 'c'*50
    tt.both_are_equal(result, expected)
    
    result = trim_long_str(x, nTab=5)
    expected = 'a'*50 + '...\n\n     [25 more chars]\n\n...' + 'c'*50
    tt.both_are_equal(result, expected)


def Test_with_escaped_chars():
    x = '12345678\nabc123456\n890'
    result = trim_long_str(repr(x), max_char=20)
    expected = "'12345678\\" + '...\n\n   [6 more chars]\n\n...' + "3456\\n890'"
    tt.both_are_equal(result, expected)


def Test_using_repr_and_return_original():
    x = 'hi 123'
    result = trim_long_str(repr(x))
    expected = repr(x)
    tt.both_are_equal(result, expected)
