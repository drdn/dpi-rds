# Internet Archive Metadata Scraper

## Requirements:
The following modules are required: internetarchive, json, csvkit, urllib.

## Usage:
**md-id.py** will create a list of identifiers using two arguments, search term and output file name.

  `$ python md-id.py foo bar.txt`

**md-scraper.py** will create a .csv of selected metadata using a list of identifiers.
Metadata fields pulled: identifier, addeddate, downloads, title, subject, and collection.

  `$ python md-scraper.py bar.txt`

## Known issues:
`csvkit` v.1.0.1 does not work with this code. Please use v.0.9.1 if possible. 
