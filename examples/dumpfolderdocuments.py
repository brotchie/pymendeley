#!/usr/bin/env python
"""
Copies all the files associated with documents in
a given folder to a destination directory.

Example:
    # mkdir -p /var/tmp/debtdocs
    # ./dumpfoldercontents.py Confirmation/Debt /var/tmp/debtdocs

"""

from __future__ import print_function

import sys
import urllib
import shutil
import os
import mendeley

def main():
    assert len(sys.argv) == 3, 'Usage: {0} folder destination'.format(sys.argv[0])
    folder, destination = sys.argv[1:3]

    assert os.path.exists(destination), 'Destination path "{0}" does not exist.'.format(destination)

    db = mendeley.MendeleyDatabaseInterface()
    for reference in db.get_references_in_folder(folder):
        urlpath = db.get_reference_path(reference)
        if urlpath:
            assert urlpath.startswith('file://')
            fspath = urllib.unquote(urlpath)[len('file://'):]

            assert os.path.exists(fspath), 'Document file "{0}" does not exist'.format(fspath.encode('utf8'))
            print('Copying from "{0}" into "{1}".'.format(fspath, destination))
            shutil.copy(fspath, destination)

if __name__ == '__main__':
    main()
