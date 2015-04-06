"""Tests for pairtree.py"""

import os

from shutil import rmtree

import pytest

from pypairtree import pairtree


TEST_DIR = os.path.dirname(__file__)


STATIC_DIR = os.path.join(TEST_DIR, 'static')


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


def test_create_paired_dir_even():
    """Checks for even directory created."""
    os.mkdir(STATIC_DIR)
    try:
        new_path = pairtree.create_paired_dir(STATIC_DIR,
                                              'coda246',
                                              static=True,
                                              needwebdir=False)
        assert new_path == os.path.join(STATIC_DIR, 'even/co/da/24/6/coda246')
        assert os.path.isdir(new_path)
    finally:
        # make sure we delete the directory created
        rmtree(STATIC_DIR)


def test_create_paired_dir_odd():
    """Checks for odd directory created."""
    os.mkdir(STATIC_DIR)
    try:
        new_path = pairtree.create_paired_dir(STATIC_DIR,
                                              'coda24a',
                                              static=True,
                                              needwebdir=False)
        assert new_path == os.path.join(STATIC_DIR, 'odd/co/da/24/a/coda24a')
        assert os.path.isdir(new_path)
    finally:
        rmtree(STATIC_DIR)


def test_create_paired_dir_web():
    """Checks for web directory created."""
    os.mkdir(STATIC_DIR)
    try:
        new_path = pairtree.create_paired_dir(STATIC_DIR,
                                              'coda242',
                                              static=True,
                                              needwebdir=True)
        assert new_path == os.path.join(STATIC_DIR,
                                        'even/co/da/24/2/coda242/web')
        assert os.path.isdir(new_path)
    finally:
        rmtree(STATIC_DIR)


def test_create_paired_dir_meta():
    """Checks regular directory is created in a meta directory."""
    meta_dir = os.path.join(TEST_DIR, 'meta')
    os.mkdir(meta_dir)
    try:
        new_path = pairtree.create_paired_dir(meta_dir,
                                              'coda24a',
                                              static=False,
                                              needwebdir=False)
        assert new_path == os.path.join(meta_dir, 'co/da/24/a/coda24a')
        assert os.path.isdir(new_path)
    finally:
        rmtree(meta_dir)


def test_add_to_pairtree_all_new():
    """Checks directories are created when all pieces are new."""
    os.mkdir(STATIC_DIR)
    try:
        new_path = pairtree.add_to_pairtree(STATIC_DIR, 'coda253ba')
        assert new_path == os.path.join(STATIC_DIR, 'co/da/25/3b/a/')
        assert os.path.isdir(new_path)
    finally:
        rmtree(STATIC_DIR)


def test_add_to_pairtree_some_exist():
    """Checks directories are created when some pieces already exist."""
    os.makedirs(os.path.join(STATIC_DIR, 'co/da'))
    try:
        new_path = pairtree.add_to_pairtree(STATIC_DIR, 'coda253ba')
        assert new_path == os.path.join(STATIC_DIR, 'co/da/25/3b/a/')
        assert os.path.isdir(new_path)
    finally:
        rmtree(STATIC_DIR)


def test_get_pairtree_prefix():
    """Checks for correct string from file."""
    store_dir = os.path.join(TEST_DIR, 'store/')
    prefix = pairtree.get_pairtree_prefix(store_dir)
    assert prefix == 'ark:/67531/'
