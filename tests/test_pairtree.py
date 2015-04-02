"""Tests for pairtree.py"""

import os

from shutil import rmtree

import pytest

from pypairtree import pairtree


TEST_DIR = os.path.dirname(__file__)


@pytest.mark.parametrize('expected', [
    'co/da/pa/+/codapa+',
    'co/da/pa/codapa',
    'co/da/pa/12/codapa12',
    'co/da/9/coda9',
])
def test_findObjects(expected):
    """Checks for expected non-shorty directories."""
    pairtree_root = os.path.join(TEST_DIR,
                                 'store/pairtree_root')
    objects = pairtree.findObjects(pairtree_root)
    assert os.path.join(pairtree_root, expected) in objects


def test_findObjects_bad_path():
    """Wants empty list upon non-existent path."""
    objects = pairtree.findObjects('fakepath')
    assert not objects


def test_get_pair_path():
    """Checks for expected path."""
    path = pairtree.get_pair_path('coda1f23c')
    assert path == '/co/da/1f/23/c/coda1f23c'


def test_isShorty_true_one():
    """Verifies True for one character names."""
    assert pairtree.isShorty('a')


def test_isShorty_true_two():
    """Verifies True for two character names."""
    assert pairtree.isShorty('bc')


def test_isShorty_false():
    """Verifies False for above two character names."""
    assert not pairtree.isShorty('codaboy')


def test_pair_tree_creator():
    """Checks for the correct pairtree string"""
    path = pairtree.pair_tree_creator('coda1f23c')
    assert path == '/co/da/1f/23/c/'


def test_deSanitizeString():
    """Checks characters from tables are replaced."""
    old_string = pairtree.deSanitizeString('coda^222^3c^2b=^2c^7c')
    assert old_string == 'coda"2<+/,|'


def test_sanitizeString():
    """Checks that string is coverted correctly."""
    new_string = pairtree.sanitizeString('coda"2<+/,|')
    assert new_string == 'coda^222^3c^2b=^2c^7c'


def test_toPairTreePath():
    """Checks for string sanitization and pairtree path format."""
    path = pairtree.toPairTreePath('coda"2<+/,|')
    assert path == 'co/da/^2/22/^3/c^/2b/=^/2c/^7/c/'


def test_create_paired_dir():
    """Checks for even directory created."""
    static_dir = os.path.join(TEST_DIR, 'static')
    os.mkdir(static_dir)
    try:
        new_path = pairtree.create_paired_dir(static_dir,
                                              'coda246',
                                              static=True,
                                              needwebdir=False)
        assert new_path == os.path.join(static_dir, 'even/co/da/24/6/coda246')
        assert os.path.isdir(new_path)
    finally:
        # make sure we delete the directory created
        rmtree(static_dir)
