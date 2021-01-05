"""Test plant morphism trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from tests.setup import test


class TestMorphism(unittest.TestCase):
    """Test plant surface trait matcher."""

    def test_morphism_01(self):
        self.assertEqual(
            test('type of the inflorescence heteropmorphic.'),
            [{'part': 'inflorescence', 'morphism': 'heteropmorphic',
              'trait': 'morphism', 'start': 0, 'end': 40}]
        )
