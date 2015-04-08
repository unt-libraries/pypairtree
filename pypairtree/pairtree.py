"""Functions for working with pairtrees.

This module provides functions for creating, traversing, and
working with Pairtree filesystem hierarchy structures.

"""

import os


sanitizerNum = 0x7d


def findObjects(path):
    """Finds objects in pairtree.

    Given a path that corresponds to a pairtree, walk it and look for
    non-shorty (it's ya birthday) directories.
    """
    objects = []
    if not os.path.isdir(path):
        return []
    contents = os.listdir(path)
    for item in contents:
        fullPath = os.path.join(path, item)
        if not os.path.isdir(fullPath):
            # deal with a split end at this point
            # we might want to consider a normalize option
            return [path]
        else:
            if isShorty(item):
                objects = objects + findObjects(fullPath)
            else:
                objects.append(fullPath)
    return objects


def get_pair_path(meta_id):
    """Determines the pair path for the digital object meta-id."""
    pair_tree = pair_tree_creator(meta_id)
    pair_path = os.path.join(pair_tree, meta_id)
    return pair_path


def isShorty(name):
    """Checks if it is a valid shorty name."""
    nLen = len(name)
    return nLen == 1 or nLen == 2


def pair_tree_creator(meta_id):
    """Splits string into a pairtree path."""
    chunks = []
    for x in xrange(0, len(meta_id)):
        if x % 2:
            continue
        if (len(meta_id) - 1) == x:
            chunk = meta_id[x]
        else:
            chunk = meta_id[x: x + 2]
        chunks.append(chunk)
    return os.sep + os.sep.join(chunks) + os.sep


def deSanitizeString(name):
    """Reverses sanitization process.

    Reverses changes made to a string that has been sanitized for use
    as a pairtree identifier.
    """
    oldString = name
    # first pass
    replaceTable2 = [
        ("/", "="),
        (":", "+"),
        (".", ","),
    ]
    for r in replaceTable2:
        oldString = oldString.replace(r[1], r[0])
    # reverse ascii 0-32 stuff
    # must subtract number added at sanitization
    for x in xrange(0, 33):
        oldString = oldString.replace(
            hex(x + sanitizerNum).replace('0x', '^'), chr(x))
    # second pass
    replaceTable = [
        ('"', '^22'),
        ('<', '^3c'),
        ('?', '^3f'),
        ('*', '^2a'),
        ('=', '^3d'),
        ('+', '^2b'),
        ('>', '^3e'),
        ('|', '^7c'),
        (',', '^2c'),
        ('^', '^5e'),
    ]

    for r in replaceTable:
        oldString = oldString.replace(r[1], r[0])
    return oldString


def sanitizeString(name):
    """Cleans string in preparation for splitting for use as a pairtree
    identifier."""
    newString = name
    # string cleaning, pass 1
    replaceTable = [
        ('^', '^5e'),  # we need to do this one first
        ('"', '^22'),
        ('<', '^3c'),
        ('?', '^3f'),
        ('*', '^2a'),
        ('=', '^3d'),
        ('+', '^2b'),
        ('>', '^3e'),
        ('|', '^7c'),
        (',', '^2c'),
    ]

    #   "   hex 22           <   hex 3c           ?   hex 3f
    #   *   hex 2a           =   hex 3d           ^   hex 5e
    #   +   hex 2b           >   hex 3e           |   hex 7c
    #   ,   hex 2c

    for r in replaceTable:
        newString = newString.replace(r[0], r[1])
    # replace ascii 0-32
    for x in xrange(0, 33):
        # must add somewhat arbitrary num to avoid conflict at deSanitization
        # conflict example: is ^x1e supposed to be ^x1 (ascii 1) followed by
        # letter 'e' or really ^x1e (ascii 30)
        newString = newString.replace(
            chr(x), hex(x + sanitizerNum).replace('0x', '^'))

    replaceTable2 = [
        ("/", "="),
        (":", "+"),
        (".", ","),
    ]

    # / -> =
    # : -> +
    # . -> ,

    # string cleaning pass 2
    for r in replaceTable2:
        newString = newString.replace(r[0], r[1])
    return newString


def toPairTreePath(name):
    """Cleans a string, and then splits it into a pairtree path."""
    sName = sanitizeString(name)
    chunks = []
    for x in xrange(0, len(sName)):
        if x % 2:
            continue
        if (len(sName) - 1) == x:
            chunk = sName[x]
        else:
            chunk = sName[x: x + 2]
        chunks.append(chunk)
    return os.sep.join(chunks) + os.sep


def create_paired_dir(output_dir, meta_id, static=False, needwebdir=True):
    """Creates the meta or static dirs.

    Adds an "even" or "odd" subdirectory to the static path
    based on the meta-id.
    """
    # get the absolute root path
    root_path = os.path.abspath(output_dir)
    # if it's a static directory, add even and odd
    if static:
        # determine whether meta-id is odd or even
        if meta_id[-1].isdigit():
            last_character = int(meta_id[-1])
        else:
            last_character = ord(meta_id[-1])
        if last_character % 2 == 0:
            num_dir = 'even'
        else:
            num_dir = 'odd'
        # add odd or even to the path, based on the meta-id
        output_path = os.path.join(root_path, num_dir)
    # if it's a meta directory, output as normal
    else:
        output_path = root_path
    # if it doesn't already exist, create the output path (includes even/odd)
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    # add the pairtree to the output path
    path_name = add_to_pairtree(output_path, meta_id)
    # add the meta-id directory to the end of the pairpath
    meta_dir = os.path.join(path_name, meta_id)
    os.mkdir(meta_dir)
    # if we are creating static output
    if static and needwebdir:
        # add the web path to the output directory
        os.mkdir(os.path.join(meta_dir, 'web'))
        static_dir = os.path.join(meta_dir, 'web')
        return static_dir
    # else we are creating meta output or don't need web directory
    else:
        return meta_dir


def add_to_pairtree(output_path, meta_id):
    """Creates pairtree dir structure within pairtree for new
    element."""
    # create the pair path
    paired_path = pair_tree_creator(meta_id)
    path_append = ''
    # for each directory in the pair path
    for pair_dir in paired_path.split(os.sep):
        # append the pair path together, one directory at a time
        path_append = os.path.join(path_append, pair_dir)
        # append the pair path to the output path
        combined_path = os.path.join(output_path, path_append)
        # if the path doesn't already exist, create it
        if not os.path.exists(combined_path):
            os.mkdir(combined_path)
    return combined_path


def get_pairtree_prefix(pairtree_store):
    """Returns the prefix given in pairtree_prefix file."""
    prefix_path = os.path.join(pairtree_store, 'pairtree_prefix')
    with open(prefix_path, 'r') as prefixf:
        prefix = prefixf.read().strip()
    return prefix
