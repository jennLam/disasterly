import unittest
import pandas as pd
import operator as op
import pandas.util.testing as pdt
from data import DisasterData


class TestCase(unittest.TestCase):

    # Create instance with test data
    test_dd = DisasterData("test_data.csv")

    def test_get_categories(self):
        """Test for get_categories."""

        expected = ['CA', 'WV', 'MT', 'DE', 'TN', 'FL', 'OR']

        actual = self.test_dd.get_categories("state")

        self.assertEqual(expected, actual)

    def test_search_criteria(self):
        """Test for search_criteria."""

        expected = pd.Series([True, True, True, False, False, True,
                             False, False, False, True, False, False], name='state', dtype='bool')
        actual = self.test_dd.search_criteria("state", "CA", op.eq)

        pdt.assert_series_equal(expected, actual)

    def test_advanced_search(self):
        """Test for advanced_search."""

    def test_make_dict(self):
        """Test for make_dict."""


if __name__ == "__main__":
    unittest.main()
