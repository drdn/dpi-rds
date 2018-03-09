#! usr/bin/env python3

#----------------------------------------------------------------------------------------
#
#   Name:           pdf-txt.py
#   Version:        v.1.1
#   Date:           2018-03-08
#   Author:         David Durden
#   Description:    Walks a given directory, finds all files with .pdf extensions,
#                   performs OCR, and saves output in a new folder as .txt using the 
#                   source file's name.
#   Usage:          python3 pdf-txt.py </path/to/directory>
#   Dependencies:   Requires the textract library
#                   <https://textract.readthedocs.io/en/stable/>
#
#----------------------------------------------------------------------------------------

from datetime import datetime
import os
import shutil
from sys import argv
import textract

# Source directory
dir = argv[1]

# Walks a given directory
for path, dirs, files in os.walk(dir):
    os.chdir(dir)
    
    # Creates new folders
    new_fdr = '{0}-txt-output'.format(
        datetime.now().strftime('%Y%m%d%H%M'))
    bad_fdr = '{0}-no-output'.format(
        datetime.now().strftime('%Y%m%d%H%M'))
    
    # Creates new paths
    new_dir = os.path.join(dir, new_fdr)
    bad_dir = os.path.join(dir, bad_fdr)
    
    # Checks if path exists, makes new directory
    if (not os.path.exists(new_dir)):
        print('Created {0}'.format(new_dir))
        os.mkdir(new_dir)
    if (not os.path.exists(bad_dir)):
        print('Created {0}'.format(bad_dir))
        os.mkdir(bad_dir)

    # Checks files, reads, generates text, creates output file
    for f in files:
        if f.endswith(('.doc', '.docx', '.html', '.pdf')):
            try:
                #fname = f.split('.', 1)[0]+'.txt'
                fname = '{0}.txt'.format(f)
                print('Created {0}'.format(fname))
                with open(fname, 'wb') as n:
                    text = textract.process(f)
                    n.write(text)
                    n.close()
                    shutil.move(fname, new_dir)
                    print('Moving {0} to {1}...'.format(fname, new_dir))
            except:
                with open('log.txt', 'w') as l:
                    log_text = 'This file ({0}) maybe corrupted or is not formatted correctly.'.format(f))
                    l.write(log_text)
                    l.close()
                shutil.move(fname, bad_dir)
        else:
            print('Not a valid format--skipping.')
            pass
