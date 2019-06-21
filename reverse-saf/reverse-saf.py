#!/usr/bin/env python3

#=============================================#
#    title: reverse-saf.py                    #
#    author: David Durden <durden@umd.edu>    #
#    version: 1.1                             #
#    date: 2019-06-21                         #
#=============================================#

import sys
import os
import requests
import urllib.request
from xml.etree import ElementTree as ET
import xml.dom.minidom as minidom

#==arguments==
file = sys.argv[1] # Supply a list of handles

#==classes==
class MissingRDFDescriptionException(Exception):
    def __str__(self):
        return "No rdf:Description found"
# To do: refactor functions with shared data as a class

#==functions==
def queryMaker(handle, prefix):
    '''
    Constructs URLs for retrieving metadata and bitstream URLs using the oai-pmh
    protocol. Prefix options are "oai-dc" for xml metadata and "ore" for rdf metadata
    with bitstream URLs.
    '''
    return "https://drum.lib.umd.edu/oai/request?verb=GetRecord&identifier=oai:drum.lib.umd.edu:1903/{0}&metadataPrefix={1}".format(handle, prefix)

def dirMaker(handle):
    '''
    Creates new directory named using handle.
    '''
    handle = handle.rstrip()
    try:
        os.makedirs(handle)
        print("Making new directory: {0}...".format(handle))
    except OSError: 
        pass
    os.chdir(handle)

def collector(handle, prefix, ext):
    '''
    Retrieves RDF XML from constructed URL using a supplied handle.
    '''
    handle = handle.rstrip()
    new_file = "{0}.{1}".format(handle, ext)
    r = requests.get(queryMaker(handle, prefix))
    print("\tGetting record: {0}...".format(handle))
    r.close
    # To do: Need a handler for items that don't exist (but really do). Looking at you
    # handle 1903/19167...
    root = ET.fromstring(r.text)
    with open(new_file, 'w') as f:
        f.write(r.text)
        print("\tWriting metadata: {0}.{1}...".format(handle, ext))
        f.close

def RDFparser(handle):
    '''
    Parses RDF for bitstream URLs and stores those URLs in a text file.
    '''
    handle = handle.strip()
    r_file = minidom.parse("{0}.rdf".format(handle))
    rElem = r_file.getElementsByTagName('rdf:Description')
    if rElem:
        parser_output = "{0}.txt".format(handle)
        for element in rElem:
            if element.childNodes[3].firstChild.nodeValue == 'ORIGINAL':
                with open(parser_output, 'a') as po:
                    po.write("{0}\n".format(element.attributes['rdf:about'].value))
                    print("\tWriting selected bitstreams to text file: {0}...".format(parser_output))
            else:
                pass
    else:
        raise MissingRDFDescriptionException()

def bitstreamDownloader(handle):
    '''
    Iterates over newly created text file, takes the bitstream URL and requests it.
    Creates a new directory named "bitstreams" in which to store... bitstreams.
    '''
    handle = handle.rstrip()
    file = '{0}.txt'.format(handle)
    bitDir = "bitstreams"
    with open(file, 'r') as f, open("error_log.txt", 'w') as er:
        dirMaker(bitDir)
        for line in f:
            line = line.strip()
            if line.find('/'):
                file_name = line.rsplit('/', 1)[-1]
                head = requests.head(line, allow_redirects=True)
                size = int(head.headers['Content-Length'])
                print("{0} is {1} bytes".format(file_name, size))
                GB = 2**30
                if size < GB/4:
                    print("\tDownloading {0}...".format(file_name))
                    r = requests.get(line)
                    open(file_name, 'wb').write(r.content)
                    # To do : Should probably check file size and request user input to 
                    # continue for files larger than 2GB...
                else:
                    print("NO! Do not want!")
                    er.write(f"{file_name} {size}\n")

# To do: Need to define a function to write XML to CSV

#==code==
with open(file, 'r') as f:
    path = "/Users/durden/Desktop" # To do: Change this to an argument
    for row in f:
        dirMaker(row)
        collector(row, 'oai_dc', 'xml')
        collector(row, 'ore', 'rdf')
        try: 
            RDFparser(row)
            bitstreamDownloader(row)
        except MissingRDFDescriptionException as e:
            print(e)
        finally:
            os.chdir(path)
    print("Done!")