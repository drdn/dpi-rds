#!/usr/bin/env python3

#----------------------------------------------------------------------------------------
#
#   Name:           md-id.py
#   Version:        v.2
#   Date:           2016-00-00
#   Author:         David Durden
#   Description:    Searches the Internet Archive for a provided term and generates
#                   a list of item ids related to that serach term.
#   Usage:          python3 md-id.py foo bar.txt
#   Dependencies:   Requires the internetarchive library
#                   <https://pypi.python.org/pypi/internetarchive>
#
#----------------------------------------------------------------------------------------

import sys
from internetarchive import search_items

# Search the Internet Archive for the first argument
term = sys.argv[1]
print("Searching IA for %s..." % term)
results = search_items('collection:%s' % term)
sys.stdout.flush()

# Convert the result to a list of ids
identifiers = [i['identifier'] for i in results]
found = "Found {0} identifiers."
print(found.format(len(identifiers)))

# Write the list of ids to the file specified by the second argument
with open(sys.argv[2], 'wt') as outfile:
    writing = "Writing to file {0} ..."
    print(writing.format(sys.argv[2]),)
    sys.stdout.flush()
    outfile.write('\n'.join(identifiers))
    print("done!")
