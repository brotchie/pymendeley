#!/usr/bin/env python
"""
Prints the path to the mendeley sqlite database.

"""
from __future__ import print_function

import sys
from mendeley import find_mendeley_sqlite_path

def main():
    path = find_mendeley_sqlite_path()

    if path:
        print(path)
        sys.exit(0)
    else:
        print('Cannot find the Mendeley sqlite3 database.')
        sys.exit(1)

if __name__ == '__main__':
    main()
