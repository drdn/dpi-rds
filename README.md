## Internet Archive Metadata Collector

#### Usage:
**md-id.py** creates a list of identifiers using two arguments, search term and output file name. 

*This script requires the Internet Archive Python library.*

  `$ python md-id.py foo bar.txt`

**md-scraper.py** creates a csv of selected metadata using a list of previously collected identifiers.
Metadata fields pulled: identifier, addeddate, downloads, title, subject, and collection.

  `$ python md-scraper.py bar.txt`
  




