import TurboTest as tt
from . import time_quick


def Awesome():

    # print('TT testing: Awesome')

    result = time_quick(0)
    expected = '0m0.0s'
    tt.both_are_equal(result, expected)
    
    result = time_quick(-1)
    expected = '0m1.0s'
    tt.both_are_equal(result, expected)
    
    result = time_quick(1)
    expected = '0m1.0s'
    tt.both_are_equal(result, expected)
    
    result = time_quick(0.1)
    expected = '0m0.1s'
    tt.both_are_equal(result, expected)
    
    result = time_quick(2.13)
    expected = '0m2.1s'
    tt.both_are_equal(result, expected)
    
    result = time_quick(61.1)
    expected = '1m1.1s'
    tt.both_are_equal(result, expected)
    
    result = time_quick(3600)
    expected = '60m0.0s'
    tt.both_are_equal(result, expected)


## TT Testing purposes
# print(locals())
# exec('from kit.readable.time_quick import time_quick')
# print(locals())
