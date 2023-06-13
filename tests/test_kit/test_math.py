from .. import add_path
add_path()


import math
import numpy as np
import unittest

from mykit.kit.math import (
    tanh,
    sigmoid,
    relu,
    get_angle,
    rotate
)


class TestMaths(unittest.TestCase):

    def test_tanh(self):

        result = tanh(0)
        self.assertAlmostEqual(result, 0)

        result = tanh(0.345)
        self.assertAlmostEqual(result, 0.33193385350364046)

        result = tanh(0.345, True)
        self.assertAlmostEqual(result, 0.8898199168982237)


        result = tanh(np.array([-2, 0, 2]))
        np.testing.assert_almost_equal(result, [-0.9640275800758169, 0.0, 0.9640275800758169])

        result = tanh(np.array([-2, 0, 2]), True)
        np.testing.assert_almost_equal(result, [0.07065082485316443, 1.0, 0.07065082485316443])

    def test_sigmoid(self):

        result = sigmoid(0.1)
        self.assertAlmostEqual(result, 0.52497918747894)

        result = sigmoid(-3, True)
        self.assertAlmostEqual(result, 0.04517665973091214)


        result = sigmoid(np.array([1, 2, 3]))
        np.testing.assert_almost_equal(result, [0.7310585786300049, 0.8807970779778823, 0.9525741268224334])

        result = sigmoid(np.array([-100, 0.4, 2000]), True)
        np.testing.assert_almost_equal(result, [3.7200759760208356e-44, 0.24026074574152914, 0.0])

    def test_relu(self):

        result = relu(-1)
        self.assertEqual(result, 0)

        result = relu(0)
        self.assertEqual(result, 0)

        result = relu(0.001)
        self.assertEqual(result, 0.001)

        result = relu(2)
        self.assertEqual(result, 2)

        result = relu(-2, True)
        self.assertEqual(result, 0)

        result = relu(2, True)
        self.assertEqual(result, 1)


        result = relu(np.array([-10, -1, -0.1, 0, 0.1, 1, 10]))
        np.testing.assert_equal(result, [0.0, 0.0, 0.0, 0.0, 0.1, 1.0, 10.0])

        result = relu(np.array([-10, -1, -0.1, 0, 0.1, 1, 10]), True)
        np.testing.assert_equal(result, [0, 0, 0, 0, 1, 1, 1])
    
    def test_get_angle(self):

        result = get_angle(0, 0, 0, 1, False)
        self.assertAlmostEqual(result, 0.0)

        result = get_angle(0, 0, -1, 0, False)
        self.assertAlmostEqual(result, 90.0)

        result = get_angle(0, 0, 0, -1, False)
        self.assertAlmostEqual(result, 180.0)

        result = get_angle(0, 0, 1, 0, False)
        self.assertAlmostEqual(result, 270.0)

        result = get_angle(0, 0, -1, 1, False)
        self.assertAlmostEqual(result, 45.0)

        result = get_angle(0, 0, -1, 1)
        self.assertAlmostEqual(result, math.pi/4)
    
    def test_rotate(self):

        ## rotate point (2, 2) around center (0, 0) by 90 degrees
        x, y = rotate(2, 2, 0, 0, math.pi/2)
        self.assertAlmostEqual(x, -2)
        self.assertAlmostEqual(y, 2)

        ## rotate point (3, 4) around center (-1, 1) by 45 degrees
        x, y = rotate(3, 4, -1, 1, math.pi/4)
        self.assertAlmostEqual(x, -0.29289321881345254)
        self.assertAlmostEqual(y, 5.949747468305834)

        ## rotate point (0, 0) around center (1, 1) by 180 degrees
        x, y = rotate(0, 0, 1, 1, math.pi)
        self.assertAlmostEqual(x, 2)
        self.assertAlmostEqual(y, 2)

        ## rotate point (5, 0) around center (2, -2) by -90 degrees
        x, y = rotate(5, 0, 2, -2, -math.pi/2)
        self.assertAlmostEqual(x, 4)
        self.assertAlmostEqual(y, -5)


if __name__ == '__main__':
    unittest.main()