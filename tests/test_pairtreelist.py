"""Tests for pairtreelist.py"""

import os

import pytest

from pypairtree import pairtreelist


@pytest.mark.parametrize('expected', [
    'ark:/67531/codapa:',
    'ark:/67531/codapa',
    'ark:/67531/codapa12',
    'ark:/67531/coda9',
])
def test_listIDs(capfd, expected):
    """Checks for listing and sanitization of pairtree objects."""
    store_dir = os.path.join(os.path.dirname(__file__), 'store')
    pairtreelist.listIDs(store_dir)
    out, err = capfd.readouterr()
    assert expected in out
