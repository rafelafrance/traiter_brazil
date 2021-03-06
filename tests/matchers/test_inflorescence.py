"""Test plant inflorescence trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from tests.setup import test


class TestMorphism(unittest.TestCase):
    """Test plant inflorescence trait matcher."""

    def test_inflorescence_01(self):
        self.assertEqual(
            test('Inflorescence: raceme congested;'),
            [{'part': 'inflorescence', 'trait': 'part', 'start': 0, 'end': 14},
             {'part': 'inflorescence', 'inflorescence': 'congested',
              'trait': 'inflorescence', 'start': 15, 'end': 31}]
        )

    def test_inflorescence_02(self):
        self.assertEqual(
            test('Inflorescence: raceme lax;'),
            [{'part': 'inflorescence', 'trait': 'part', 'start': 0, 'end': 14},
             {'part': 'inflorescence', 'inflorescence': 'lax',
              'trait': 'inflorescence', 'start': 15, 'end': 25}]
        )
