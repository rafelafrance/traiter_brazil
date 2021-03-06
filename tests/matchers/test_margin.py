"""Test plant margin trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from tests.setup import test


class TestMargin(unittest.TestCase):
    """Test plant margin trait matcher."""

    def test_margin_01(self):
        self.assertEqual(
            test('Fruit: margin smooth or sinuose the irregularly constricted.'),
            [{'part': 'fruit', 'trait': 'part', 'start': 0, 'end': 6},
             {'subpart': 'margin', 'part': 'fruit',
              'margin': ['smooth', 'sinuose', 'irregularly constricted'],
              'trait': 'margin', 'start': 7, 'end': 59}]
        )

    def test_margin_02(self):
        self.assertEqual(
            test('Fruit: margin moniliform.'),
            [{'part': 'fruit', 'trait': 'part', 'start': 0, 'end': 6},
             {'subpart': 'margin', 'margin': 'moniliform', 'part': 'fruit',
              'trait': 'margin', 'start': 7, 'end': 24}]
        )
