import unittest

from mykit.kit.utils import (
    sort_dict_by_key, sort_dict_by_val,
    get_first_n_dict_items, get_last_n_dict_items,
    reverse_dict,
    merge_dicts, merging_dicts,
    add_dict_val
)


class Test__sort_dict_by_key(unittest.TestCase):

    def test_reverse0(self):

        d = {
            'b': 0,
            'a': 0,
            'c': 0,
        }
        result = sort_dict_by_key(d)
        expected = {
            'a': 0,
            'b': 0,
            'c': 0,
        }
        self.assertEqual(result, expected)

        d = {
            2: '',
            1: '',
            3: '',
        }
        result = sort_dict_by_key(d)
        expected = {
            1: '',
            2: '',
            3: '',
        }
        self.assertEqual(result, expected)

    def test_reverse1(self):

        d = {
            'b': 0,
            'a': 0,
            'c': 0,
        }
        result = sort_dict_by_key(d, 1)
        expected = {
            'c': 0,
            'b': 0,
            'a': 0,
        }
        self.assertEqual(result, expected)

        d = {
            2: '',
            1: '',
            3: '',
        }
        result = sort_dict_by_key(d, 1)
        expected = {
            3: '',
            2: '',
            1: '',
        }
        self.assertEqual(result, expected)


class Test__sort_dict_by_val(unittest.TestCase):

    def test_reverse0(self):

        d = {
            1: 'b',
            2: 'a',
            3: 'c',
        }
        result = sort_dict_by_val(d)
        expected = {
            2: 'a',
            1: 'b',
            3: 'c',
        }
        self.assertEqual(result, expected)

        d = {
            'a': 2,
            'b': 1,
            'c': 3,
        }
        result = sort_dict_by_val(d)
        expected = {
            'b': 1,
            'a': 2,
            'c': 3,
        }
        self.assertEqual(result, expected)

    def test_reverse1(self):

        d = {
            1: 'b',
            2: 'a',
            3: 'c',
        }
        result = sort_dict_by_val(d, 1)
        expected = {
            3: 'c',
            1: 'b',
            2: 'a',
        }
        self.assertEqual(result, expected)

        d = {
            'a': 2,
            'b': 1,
            'c': 3,
        }
        result = sort_dict_by_val(d, 1)
        expected = {
            'c': 3,
            'a': 2,
            'b': 1,
        }
        self.assertEqual(result, expected)


class Test__get_first_n_dict_items(unittest.TestCase):

    def test(self):

        d = {
            'apple': 5,
            'banana': 3,
            'cherry': 8,
        }

        result = get_first_n_dict_items(d, -1)
        expected = {}
        self.assertEqual(result, expected)

        result = get_first_n_dict_items(d, 0)
        expected = {}
        self.assertEqual(result, expected)

        result = get_first_n_dict_items(d, 1)
        expected = {'apple': 5}
        self.assertEqual(result, expected)

        result = get_first_n_dict_items(d, 2)
        expected = {
            'apple': 5,
            'banana': 3,
        }
        self.assertEqual(result, expected)

        result = get_first_n_dict_items(d, 3)
        expected = {
            'apple': 5,
            'banana': 3,
            'cherry': 8,
        }
        self.assertEqual(result, expected)

        result = get_first_n_dict_items(d, 4)
        expected = {
            'apple': 5,
            'banana': 3,
            'cherry': 8,
        }
        self.assertEqual(result, expected)

        result = get_first_n_dict_items(d, 10)
        expected = {
            'apple': 5,
            'banana': 3,
            'cherry': 8,
        }
        self.assertEqual(result, expected)


class Test__get_last_n_dict_items(unittest.TestCase):

    def test(self):

        d = {
            'apple': 5,
            'banana': 3,
            'cherry': 8,
        }

        result = get_last_n_dict_items(d, -1)
        expected = {}
        self.assertEqual(result, expected)

        result = get_last_n_dict_items(d, 0)
        expected = {}
        self.assertEqual(result, expected)

        result = get_last_n_dict_items(d, 1)
        expected = {'cherry': 8}
        self.assertEqual(result, expected)

        result = get_last_n_dict_items(d, 2)
        expected = {
            'banana': 3,
            'cherry': 8,
        }
        self.assertEqual(result, expected)

        result = get_last_n_dict_items(d, 3)
        expected = {
            'apple': 5,
            'banana': 3,
            'cherry': 8,
        }
        self.assertEqual(result, expected)

        result = get_last_n_dict_items(d, 4)
        expected = {
            'apple': 5,
            'banana': 3,
            'cherry': 8,
        }
        self.assertEqual(result, expected)

        result = get_last_n_dict_items(d, 10)
        expected = {
            'apple': 5,
            'banana': 3,
            'cherry': 8,
        }
        self.assertEqual(result, expected)


class Test__reverse_dict(unittest.TestCase):

    def test(self):

        d = {
            'apple': 5,
            'banana': 3,
            'cherry': 8,
        }
        result = reverse_dict(d)
        expected = {
            'cherry': 8,
            'banana': 3,
            'apple': 5,
        }
        self.assertEqual(result, expected)

        d = {
            5: '',
            3: '',
            9: '',
        }
        result = reverse_dict(d)
        expected = {
            9: '',
            3: '',
            5: '',
        }
        self.assertEqual(result, expected)


class Test__merge_dicts(unittest.TestCase):

    def test_1(self):

        dict1 = {'a': 1, 'b': 2, 'c': 3}
        dict2 = {'b': 3, 'c': 4, 'd': 5}

        result = merge_dicts(dict1, dict2)
        expected = {'a': 1, 'b': 5, 'c': 7, 'd': 5}
        self.assertEqual(result, expected)

        ## Both input dictionaries should be preserved
        self.assertEqual(
            dict1,
            {'a': 1, 'b': 2, 'c': 3}
        )
        self.assertEqual(
            dict2,
            {'b': 3, 'c': 4, 'd': 5}
        )

    def test_2(self):

        dict1 = {}
        dict2 = {'b': 3, 'c': 4, 'd': 5}

        result = merge_dicts(dict1, dict2)
        expected = {'b': 3, 'c': 4, 'd': 5}
        self.assertEqual(result, expected)

        ## Both input dictionaries should be preserved
        self.assertEqual(
            dict1,
            {}
        )
        self.assertEqual(
            dict2,
            {'b': 3, 'c': 4, 'd': 5}
        )
    
    def test_3(self):

        dict1 = {'a': 1, 'b': 2, 'c': 3}
        dict2 = {}

        result = merge_dicts(dict1, dict2)
        expected = {'a': 1, 'b': 2, 'c': 3}
        self.assertEqual(result, expected)

        ## Both input dictionaries should be preserved
        self.assertEqual(
            dict1,
            {'a': 1, 'b': 2, 'c': 3}
        )
        self.assertEqual(
            dict2,
            {}
        )


class Test__merging_dicts(unittest.TestCase):

    def test_1(self):

        dict1 = {'a': 1, 'b': 2, 'c': 3}
        dict2 = {'b': 3, 'c': 4, 'd': 5}

        merging_dicts(dict1, dict2)

        self.assertEqual(
            dict1,
            {'a': 1, 'b': 5, 'c': 7, 'd': 5}
        )
        self.assertEqual(
            dict2,
            {'b': 3, 'c': 4, 'd': 5}
        )

    def test_2(self):

        dict1 = {}
        dict2 = {'b': 3, 'c': 4, 'd': 5}

        merging_dicts(dict1, dict2)

        self.assertEqual(
            dict1,
            {'b': 3, 'c': 4, 'd': 5}
        )
        self.assertEqual(
            dict2,
            {'b': 3, 'c': 4, 'd': 5}
        )

    def test_3(self):

        dict1 = {'a': 1, 'b': 2, 'c': 3}
        dict2 = {}

        merging_dicts(dict1, dict2)

        self.assertEqual(
            dict1,
            {'a': 1, 'b': 2, 'c': 3}
        )
        self.assertEqual(
            dict2,
            {}
        )


class Test__add_dict_val(unittest.TestCase):

    def test_key_exists(self):

        d = {
            'a': 0,
            'b': 5,
        }
        add_dict_val(d, 'a')
        expected = {
            'a': 1,
            'b': 5,
        }
        self.assertEqual(d, expected)

        d = {
            'a': 0,
            'b': 5,
        }
        add_dict_val(d, 'a', 1000)
        expected = {
            'a': 1000,
            'b': 5,
        }
        self.assertEqual(d, expected)

    def test_key_does_not_exist(self):

        d = {
            'a': 0,
            'b': 5,
        }
        add_dict_val(d, 'c')
        expected = {
            'a': 0,
            'b': 5,
            'c': 1,
        }
        self.assertEqual(d, expected)

        d = {
            'a': 0,
            'b': 5,
        }
        add_dict_val(d, 'c', 10, 20)
        expected = {
            'a': 0,
            'b': 5,
            'c': 20,
        }
        self.assertEqual(d, expected)


if __name__ == '__main__':
    unittest.main()