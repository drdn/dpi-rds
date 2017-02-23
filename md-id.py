#!/usr/bin/python
#IDENTIFIER GENERATOR - Internet Archive

from internetarchive import search_items
import sys

#search IA for the first argument
term = sys.argv[1]
print "Searching IA for %s..." % term
results = search_items('collection:%s' % term)
#results = search_items(sys.argv[1])
sys.stdout.flush()

# convert the result to a list of ids
identifiers = [i['identifier'] for i in results]
found = "Found {0} identifiers."
print found.format(len(identifiers))

# write the list of ids to the file specified by the 2nd argument
with open(sys.argv[2], 'wt') as outfile:
    writing = "Writing to file {0} ..."
    print writing.format(sys.argv[2]),
    sys.stdout.flush()
    outfile.write('\n'.join(identifiers))
    fin = "done!"
    print fin
