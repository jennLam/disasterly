import unittest
import pandas as pd
import operator as op
import pandas.util.testing as pdt
from data import DisasterData


class TestCase(unittest.TestCase):

    # Create instance with test data
    test_dd = DisasterData()

    def test_get_categories(self):
        """Test for get_categories."""

    def test_search_criteria(self):
        """Test for search_criteria."""

    def test_advanced_search(self):
        """Test for advanced_search."""

    def test_make_dict(self):
        """Test for make_dict."""


if __name__ == "__main__":
    unittest.main()
