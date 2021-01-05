"""Common utility functions for Brazil Flora"""

from src.pylib.consts import BRAZIL_DIR, CONVERT


def species_path(family):
    """Build the path to the list of species for the family."""
    return BRAZIL_DIR / f'{family.capitalize()}_species.json'


def convert(number, units):
    """Normalize the units to meters."""
    return number * CONVERT.get(units, 1.0)
