#!/usr/bin/env python

"""Provides a function to print object identifiers in a Pairtree.

__main__ function allows this to be run from the commandline.
"""

import os
import sys

from optparse import OptionParser

from pypairtree import pairtree


def listIDs(basedir):
    """Lists digital object identifiers of Pairtree directory structure.

    Walks a Pairtree directory structure to get IDs. Prepends prefix
    found in pairtree_prefix file. Outputs to standard output.
    """
    prefix = ''
    # check for pairtree_prefix file
    prefixfile = os.path.join(basedir, 'pairtree_prefix')
    if os.path.isfile(prefixfile):
        rff = open(prefixfile, 'r')
        prefix = rff.readline().strip()
        rff.close()
    # check for pairtree_root dir
    root = os.path.join(basedir, 'pairtree_root')
    if os.path.isdir(root):
        objects = pairtree.findObjects(root)
        for obj in objects:
            doi = os.path.split(obj)[1]
            # print with prefix and original chars in place
            print prefix + pairtree.deSanitizeString(doi)
    else:
        print 'pairtree_root directory not found'


if __name__ == '__main__':
    usage = 'usage: %prog [options] <pairtreedir>'
    parser = OptionParser(usage)
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.print_help()
        sys.exit(1)
    listIDs(args[0])
