import unittest

from mykit.kit.color import (
    interpolate_color,
    getgray,
    rgb_to_hex,
    hexa_to_hex,
    interpolate_with_black,
    hex_to_rgb,
    colored_len, Colored, Hex
)


class Test__Color(unittest.TestCase):

    def test_interpolate_color(self):
        
        ## regular cases

        result = interpolate_color('#ff0000', '#0000ff', 0.0)
        self.assertEqual(result, '#ff0000')

        result = interpolate_color('#ff0000', '#0000ff', 0.5)
        self.assertEqual(result, '#800080')

        result = interpolate_color('#ff0000', '#0000ff', 1.0)
        self.assertEqual(result, '#0000ff')


        ## extreme cases

        result = interpolate_color('#000000', '#ffffff', 0.0)
        self.assertEqual(result, '#000000')

        result = interpolate_color('#000000', '#ffffff', 1.0)
        self.assertEqual(result, '#ffffff')

        result = interpolate_color('#000000', '#000000', 0.5)
        self.assertEqual(result, '#000000')

        result = interpolate_color('#ffffff', '#ffffff', 0.8)
        self.assertEqual(result, '#ffffff')
    
    def test_getgray(self):

        result = getgray(0.5)
        self.assertEqual(result, '#808080')

        result = getgray(0)
        self.assertEqual(result, '#000000')

        result = getgray(1, max_lum=200)
        self.assertEqual(result, '#c8c8c8')

        result = getgray(0.75, max_lum=100)
        self.assertEqual(result, '#4b4b4b')

    def test_rgb_to_hex(self):

        ## black color (all channels set to 0)
        result = rgb_to_hex(0, 0, 0)
        self.assertEqual(result, '#000000')

        ## white color (all channels set to 255)
        result = rgb_to_hex(255, 255, 255)
        self.assertEqual(result, '#ffffff')

        ## red color (only red channel set to 255)
        result = rgb_to_hex(255, 0, 0)
        self.assertEqual(result, '#ff0000')

        ## green color (only green channel set to 255)
        result = rgb_to_hex(0, 255, 0)
        self.assertEqual(result, '#00ff00')

        ## blue color (only blue channel set to 255)
        result = rgb_to_hex(0, 0, 255)
        self.assertEqual(result, '#0000ff')

        ## custom color (random channel values)
        result = rgb_to_hex(100, 150, 200)
        self.assertEqual(result, '#6496c8')

        ## boundary values (minimum and maximum channel values)
        result = rgb_to_hex(0, 255, 127)
        self.assertEqual(result, '#00ff7f')

        ## negative channel values
        result = rgb_to_hex(-10, 0, 255)
        self.assertEqual(result, '#-a00ff')

        ## large channel values
        result = rgb_to_hex(1000, 500, 2550)
        self.assertEqual(result, '#3e81f49f6')
    
    def test_hexa_to_hex(self):

        result = hexa_to_hex('#ffffff', 0, '#000000')
        self.assertEqual(result, '#000000')

        result = hexa_to_hex('#ffffff', 0.5, '#000000')
        self.assertEqual(result, '#808080')

        result = hexa_to_hex('#ffffff', 1, '#000000')
        self.assertEqual(result, '#ffffff')


        result = hexa_to_hex('#abcabc', 0, '#abcabc')
        self.assertEqual(result, '#abcabc')

        result = hexa_to_hex('#abcabc', 0.5, '#abcabc')
        self.assertEqual(result, '#abcabc')

        result = hexa_to_hex('#abcabc', 1, '#abcabc')
        self.assertEqual(result, '#abcabc')


        result = hexa_to_hex('#112233', 0.25, '#aabbcc')
        self.assertEqual(result, '#8495a6')

        result = hexa_to_hex('#ccddee', 0.345, '#123456')
        self.assertEqual(result, '#526e8a')
    
    def test_interpolate_with_black(self):

        result = interpolate_with_black('#ffffff', 0)
        self.assertEqual(result, '#000000')

        result = interpolate_with_black('#ffffff', 0.5)
        self.assertEqual(result, '#808080')

        result = interpolate_with_black('#ffffff', 1)
        self.assertEqual(result, '#ffffff')


        result = interpolate_with_black('#131313', 0.8)
        self.assertEqual(result, '#0f0f0f')

        result = interpolate_with_black('#abc123', 0.234)
        self.assertEqual(result, '#282d08')


class Test__hex_to_rgb(unittest.TestCase):

    def test(self):

        result = hex_to_rgb('#000000')
        expected = (0, 0, 0)
        self.assertEqual(result, expected)

        result = hex_to_rgb('#ffffff')
        expected = (255, 255, 255)
        self.assertEqual(result, expected)

        result = hex_to_rgb('#ff0000')
        expected = (255, 0, 0)
        self.assertEqual(result, expected)

        result = hex_to_rgb('#abcdef')
        expected = (171, 205, 239)
        self.assertEqual(result, expected)


class Test__colored_len(unittest.TestCase):

    def test(self):

        text = 'hi'
        result = colored_len(text)
        self.assertEqual(result, 2)

        text = Colored('hi')
        result = colored_len(text)
        self.assertEqual(result, 2)

        text = Colored('')
        result = colored_len(text)
        self.assertEqual(result, 0)

        text = Colored('12345', Hex.RED, Hex.BLACK)
        result = colored_len(text)
        self.assertEqual(result, 5)

        text = '123' + Colored('45', Hex.RED, Hex.BLACK) + '67'
        result = colored_len(text)
        self.assertEqual(result, 7)

        text = '123' + Colored('45', Hex.RED, Hex.BLACK) + '67' + Colored('89')
        result = colored_len(text)
        self.assertEqual(result, 9)

        text = Colored('12' + Colored('345', Hex.GREEN))
        result = colored_len(text)
        self.assertEqual(result, 5)

        text = Colored('12' + Colored('345', Hex.GREEN, Hex.BLACK)) + '67'
        result = colored_len(text)
        self.assertEqual(result, 7)


if __name__ == '__main__':
    unittest.main()
