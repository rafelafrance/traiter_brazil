"""Test plant size trait matcher."""

import unittest

from tests.setup import test


class TestSize(unittest.TestCase):
    """Test plant size trait matcher."""

    def test_size_01(self):
        self.assertEqual(
            test('size of the leaflet bigger than 1.8 cm;'),
            [{'length_low': 1.8, 'length_units': 'cm', 'part': 'leaflet',
              'plus': True, 'trait': 'size', 'start': 0, 'end': 38}]
        )

    def test_size_02(self):
        self.assertEqual(
            test('size of the leaflet to 1.8 cm;'),
            [{'length_low': 1.8, 'length_units': 'cm', 'part': 'leaflet',
              'trait': 'size', 'start': 0, 'end': 29}]
        )

    def test_size_03(self):
        self.assertEqual(
            test('size of the leaflet to 1.4 cm/bigger than 1.8 cm;'),
            [{'length_low': 1.4, 'length_high': 1.8, 'length_units': 'cm',
              'plus': True, 'part': 'leaflet', 'trait': 'size',
              'start': 0, 'end': 48}]
        )

    def test_size_04(self):
        self.assertEqual(
            test('size of the leaflet to 1.8 cm/bigger than 1.8 cm;'),
            [{'length_low': 1.8, 'length_units': 'cm', 'plus': True,
              'part': 'leaflet', 'trait': 'size', 'start': 0, 'end': 48}]
        )
