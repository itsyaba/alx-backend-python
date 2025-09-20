#!/usr/bin/env python3
"""Utility functions for testing project."""
from typing import Any, Mapping, Tuple
import requests

def access_nested_map(nested_map: Mapping, path: Tuple) -> Any:
    """Access a nested map with a given path."""
    for key in path:
        nested_map = nested_map[key]
    return nested_map

def get_json(url: str) -> Any:
    """Get JSON response from a URL."""
    response = requests.get(url)
    return response.json()

def memoize(fn):
    """Decorator to memoize method results."""
    attr_name = "_memoized_" + fn.__name__

    @property
    def memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return memoized
