import TurboTest as tt
from . import ctxt

from mykit.kit.color import Hex, hex_to_rgb


RED = '#ff0000'
GREEN = '#00ff00'
BLUE = '#0000ff'
YELLOW = '#ffff00'


# def Default_color():
#     r, g, b = hex_to_rgb(Hex.LAVENDER_GRAY)
#     result = repr(ctxt('hi mom'))
#     expected = f"'\\x1b[38;2;{r};{g};{b}mhi mom\\x1b[0m'"
#     tt.both_are_equal(result, expected)


# def Single_color():
#     result = repr(ctxt('hi mom', RED))
#     expected = "'\\x1b[38;2;255;0;0mhi mom\\x1b[0m'"
#     tt.both_are_equal(result, expected)


# def Single_color_and_a_plain_text():
#     result = repr(ctxt('hi mom', RED) + '123')
#     expected = "'\\x1b[38;2;255;0;0mhi mom\\x1b[0m123'"
#     tt.both_are_equal(result, expected)


# def A_plain_text_then_single_color():
#     result = repr('love you ' + ctxt('mom', RED))
#     expected = "'love you \\x1b[38;2;255;0;0mmom\\x1b[0m'"
#     tt.both_are_equal(result, expected)


# def Colored_then_plain_then_colored():
#     result = repr(ctxt('love', RED) + ' love you ' + ctxt('mom', BLUE))
#     expected = "'\\x1b[38;2;255;0;0mlove\\x1b[0m love you \\x1b[38;2;0;0;255mmom\\x1b[0m'"
#     tt.both_are_equal(result, expected)


# def Plain_then_colored_then_plain():
#     result = repr('hi ' + ctxt('love', GREEN) + ' wow')
#     expected = "'hi \\x1b[38;2;0;255;0mlove\\x1b[0m wow'"
#     tt.both_are_equal(result, expected)


# def Simple_color_in_color():
#     t1 = ctxt('hi', RED)
#     t2 = ctxt(t1 + 'mom' + t1, GREEN)
#     result = repr(t2)
#     expected = "'\\x1b[38;2;255;0;0mhi\\x1b[38;2;0;255;0mmom\\x1b[38;2;255;0;0mhi\\x1b[0m'"
#     tt.both_are_equal(result, expected)


# def Complex_color_in_color():
#     t1 = ctxt('hi', RED)
#     t2 = ctxt(t1 + 'mom' + t1, GREEN)
#     t3 = ctxt(t2 + 'okay', BLUE)
#     result = repr(t3)
#     expected = "'\\x1b[38;2;255;0;0mhi\\x1b[38;2;0;255;0mmom\\x1b[38;2;255;0;0mhi\\x1b[38;2;0;0;255mokay\\x1b[0m'"
#     tt.both_are_equal(result, expected)


# def Complex_color_in_color_II():
#     t1 = ctxt('hi', RED)
#     t2 = ctxt(t1 + 'mom' + t1, GREEN)
#     t3 = ctxt(t2 + 'okay', BLUE) + 'nocolor' + t1
#     t4 = ctxt(t3, '#ffff00')
#     result = repr(t4)
#     expected = "'\\x1b[38;2;255;0;0mhi\\x1b[38;2;0;255;0mmom\\x1b[38;2;255;0;0mhi\\x1b[38;2;0;0;255mokay\\x1b[38;2;255;255;0mnocolor\\x1b[38;2;255;0;0mhi\\x1b[0m'"
#     tt.both_are_equal(result, expected)


# def Simple_color_with_background():
#     result = repr(ctxt('hi', RED, GREEN))
#     expected = "'\\x1b[38;2;255;0;0;48;2;0;255;0mhi\\x1b[0m'"
#     tt.both_are_equal(result, expected)


# def Simple_color_with_background_then_plain():
#     result = repr(ctxt('hi', RED, GREEN) + 'mom')
#     expected = "'\\x1b[38;2;255;0;0;48;2;0;255;0mhi\\x1b[0mmom'"
#     tt.both_are_equal(result, expected)


# def Complex_color_in_color_with_background():
#     t1 = ctxt('hi', RED, BLUE)
#     t2 = ctxt(t1 + 'mom' + t1, GREEN)
#     t3 = ctxt(t2 + 'okay', BLUE) + 'nocolor' + t1
#     t4 = ctxt(t3 + 'wow', '#ffff00', GREEN) + 'really-no-color'
#     result = repr(t4)
#     expected = "'\\x1b[38;2;255;0;0;48;2;0;0;255mhi\\x1b[38;2;0;255;0mmom\\x1b[38;2;255;0;0;48;2;0;0;255mhi\\x1b[38;2;0;0;255mokay\\x1b[38;2;255;255;0;48;2;0;255;0mnocolor\\x1b[38;2;255;0;0;48;2;0;0;255mhi\\x1b[38;2;255;255;0;48;2;0;255;0mwow\\x1b[0mreally-no-color'"
#     tt.both_are_equal(result, expected)


# def The_colored_cant_get_recolored():
#     pass



## to be honest, the above tests are so painful to read

FG_RED_NO_BG = '\x1b[38;2;255;0;0mA\x1b[0m'  # A
FG_GREEN_NO_BG = '\x1b[38;2;0;255;0mB\x1b[0m'  # B
FG_BLUE_NO_BG = '\x1b[38;2;0;0;255mC\x1b[0m'  # C
FG_RED_BG_YELLOW = '\x1b[38;2;255;0;0;48;2;255;255;0mD\x1b[0m'  # D
FG_YELLOW_NO_BG = '\x1b[38;2;255;255;0mE\x1b[0m'  # E
FG_BLUE_BG_GREEN = '\x1b[38;2;0;0;255;48;2;0;255;0mF\x1b[0m'  # F
if __name__ == '__main__':  # Debugging purposes
    import os;os.system('color')
    print('x ' + FG_RED_NO_BG + ' y')
    print('x ' + FG_GREEN_NO_BG + ' y')
    print('x ' + FG_BLUE_NO_BG + ' y')
    print('x ' + FG_RED_BG_YELLOW + ' y')
    print('x ' + FG_YELLOW_NO_BG + ' y')
    print('x ' + FG_BLUE_BG_GREEN + ' y')


def Default_color():
    r, g, b = hex_to_rgb(Hex.LAVENDER_GRAY)
    result = ctxt('hi mom')
    expected = f'\x1b[38;2;{r};{g};{b}mhi mom\x1b[0m'
    tt.both_are_equal(result, expected)


def Single_color():
    result = ctxt('A', RED)
    expected = FG_RED_NO_BG
    tt.both_are_equal(result, expected)


def Single_color_and_a_plain_text():
    result = ctxt('A', RED) + 'foo'
    expected = FG_RED_NO_BG + 'foo'
    tt.both_are_equal(result, expected)


def A_plain_text_then_single_color():
    result = 'foo' + ctxt('A', RED)
    expected = 'foo' + FG_RED_NO_BG
    tt.both_are_equal(result, expected)


def Colored_then_plain_then_colored():
    result = ctxt('A', RED) + 'foo' + ctxt('B', GREEN)
    expected = FG_RED_NO_BG + 'foo' + FG_GREEN_NO_BG
    tt.both_are_equal(result, expected)


def Plain_then_colored_then_plain():
    result = 'foo' + ctxt('A', RED) + 'bar'
    expected = 'foo' + FG_RED_NO_BG + 'bar'
    tt.both_are_equal(result, expected)


def Simple_color_in_color():
    t1 = ctxt('A', RED)
    t2 = ctxt(t1 + 'B' + t1, GREEN)
    result = t2
    expected = FG_RED_NO_BG + FG_GREEN_NO_BG + FG_RED_NO_BG
    tt.both_are_equal(result, expected)


def Complex_color_in_color():
    t1 = ctxt('A', RED)
    t2 = ctxt(t1 + 'B' + t1, GREEN)
    t3 = ctxt(t2 + 'C', BLUE)
    result = t3
    expected = FG_RED_NO_BG + FG_GREEN_NO_BG + FG_RED_NO_BG + FG_BLUE_NO_BG
    tt.both_are_equal(result, expected)


def Complex_color_in_color_II():
    t1 = ctxt('A', RED)
    t2 = ctxt(t1 + 'B' + t1, GREEN)
    t3 = ctxt(t2 + 'C', BLUE) + 'E' + t1
    t4 = ctxt(t3, YELLOW)
    result = t4
    expected = FG_RED_NO_BG + FG_GREEN_NO_BG + FG_RED_NO_BG + FG_BLUE_NO_BG + FG_YELLOW_NO_BG + FG_RED_NO_BG
    tt.both_are_equal(result, expected)


def Simple_color_with_background():
    result = ctxt('D', RED, YELLOW)
    expected = FG_RED_BG_YELLOW
    tt.both_are_equal(result, expected)


def Simple_color_with_background_then_plain():
    result = ctxt('D', RED, YELLOW) + 'foo'
    expected = FG_RED_BG_YELLOW + 'foo'
    tt.both_are_equal(result, expected)


def Complex_color_in_color_with_background():
    t1 = ctxt('D', RED, YELLOW)
    t2 = ctxt(t1 + 'B' + t1, GREEN)
    t3 = ctxt(t2 + 'C', BLUE) + 'F' + t1
    t4 = ctxt(t3 + 'F', BLUE, GREEN) + 'hi'
    result = t4
    expected = FG_RED_BG_YELLOW + FG_GREEN_NO_BG + FG_RED_BG_YELLOW + FG_BLUE_NO_BG + FG_BLUE_BG_GREEN + FG_RED_BG_YELLOW + FG_BLUE_BG_GREEN + 'hi'
    tt.both_are_equal(result, expected)


def The_colored_cant_get_recolored():
    t1 = ctxt('A', RED)
    t2 = ctxt(t1, GREEN)
    result = t2
    expected = FG_RED_NO_BG
    tt.both_are_equal(result, expected)

def The_colored_cant_get_recolored_II():
    t1 = ctxt('A', RED, YELLOW)
    t2 = ctxt(t1, GREEN)
    result = t2
    expected = FG_RED_BG_YELLOW
    tt.both_are_equal(result, expected)

def The_colored_cant_get_recolored_III():
    t1 = ctxt('A', RED)
    t2 = ctxt(t1, BLUE, GREEN)
    result = t2
    expected = FG_RED_NO_BG
    tt.both_are_equal(result, expected)
