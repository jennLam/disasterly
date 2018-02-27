import unittest
import pandas as pd
import numpy as np
import operator as op
import pandas.util.testing as pdt
from collections import OrderedDict
from data import DisasterData


class TestCase(unittest.TestCase):

    # Create instance with test data
    test_dd = DisasterData("test_data.csv")

    def test_get_categories(self):
        """Test for get_categories."""

        expected = ['CA', 'FL', 'OR']

        actual = self.test_dd.get_categories("state")

        self.assertEqual(expected, actual)

    def test_search_criteria(self):
        """Test for search_criteria."""

        expected = pd.Series([True, True, True, False, True,
                             False, False], name='state', dtype='bool')
        actual = self.test_dd.search_criteria("state", "CA", op.eq)

        pdt.assert_series_equal(expected, actual)

    def test_advanced_search(self):
        """Test for advanced_search."""

        d = {'disasterNumber': {0: 183, 1: 183, 2: 183, 3: 176, 4: 183, 5: 183, 6: 184},
             'state': {0: 'CA', 1: 'CA', 2: 'CA', 3: 'FL', 4: 'CA', 5: 'OR', 6: 'OR'},
             'incidentType': {0: 'Flood',
                              1: 'Flood',
                              2: 'Flood',
                              3: 'Hurricane',
                              4: 'Flood',
                              5: 'Flood',
                              6: 'Flood'},
             'title': {0: 'HEAVY RAINS & FLOODING',
                       1: 'HEAVY RAINS & FLOODING',
                       2: 'HEAVY RAINS & FLOODING',
                       3: 'HURRICANE DORA',
                       4: 'HEAVY RAINS & FLOODING',
                       5: 'HEAVY RAINS & FLOODING',
                       6: 'HEAVY RAINS & FLOODING'},
             'incidentBeginDate': {0: pd.Timestamp('1964-12-24 00:00:00'),
                                    1: pd.Timestamp('1964-12-24 00:00:00'),
                                    2: pd.Timestamp('1964-12-24 00:00:00'),
                                    3: pd.Timestamp('1964-09-10 00:00:00'),
                                    4: pd.Timestamp('1964-12-24 00:00:00'),
                                    5: pd.Timestamp('1964-12-24 00:00:00'),
                                    6: pd.Timestamp('1964-12-24 00:00:00')},
             'incidentEndDate': {0: pd.Timestamp('1964-12-24 00:00:00'),
                                    1: pd.Timestamp('1964-12-24 00:00:00'),
                                    2: pd.Timestamp('1964-12-24 00:00:00'),
                                    3: pd.Timestamp('1964-09-10 00:00:00'),
                                    4: pd.Timestamp('1964-12-24 00:00:00'),
                                    5: pd.Timestamp('1964-12-24 00:00:00'),
                                    6: pd.Timestamp('1964-12-24 00:00:00')},
             'declaredCountyArea': {0: 'El Dorado (County)',
                                    1: 'Mendocino (County)',
                                    2: 'Nevada (County)',
                                    3: np.nan,
                                    4: 'San Joaquin (County)',
                                    5: 'Shasta (County)',
                                    6: 'Hood River (County)'}}

        expected = pd.DataFrame(data=OrderedDict(d))
        actual = self.test_dd.advanced_search()

        pdt.assert_frame_equal(expected, actual)

    def test_make_dict(self):
        """Test for make_dict."""


if __name__ == "__main__":
    unittest.main()
