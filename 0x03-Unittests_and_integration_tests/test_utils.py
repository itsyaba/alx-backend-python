"""
Unit tests for utils.py
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Tests for get_json"""

    @patch("utils.requests.get")
    def test_get_json(self, mock_get):
        mock_get.return_value.json.return_value = {"payload": True}
        self.assertEqual(get_json("http://example.com"), {"payload": True})
        mock_get.assert_called_once_with("http://example.com")


class TestMemoize(unittest.TestCase):
    """Tests for memoize"""

    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        obj = TestClass()
        self.assertEqual(obj.a_property, 42)
        self.assertEqual(obj.a_property, 42)
