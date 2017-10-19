#!/usr/bin/env python3
'''
Selective metadata collection script.'''

import sys
import urllib.request
import json
import csv
from datetime import datetime

# Variables
new_file = '%s-%s%s' % ("umd_ia_stats-", datetime.now().strftime('%Y%m%d%H%M'), ".csv")
input_file = sys.argv[1]

print('%s %s' % ('Started @', datetime.now()))

# Read ids from input file
with open(input_file, 'r') as f1:
    ids = [i.strip('\n') for i in f1.readlines()]
    print("collecting metadata for %s ids..." % range(len(ids)))
    
    with open(new_file, 'w', newline='', encoding='utf-8') as csvfile: 
        fieldnames = ['identifier', 'upload_date', 'total_views', 'title', 'topic', 'collection']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for id in ids:
            # Collect selected metadata 
            try:
                url = "http://archive.org/details/{0}&output=json".format(id) 
                data = json.loads(urllib.request.urlopen(url).read())
                jdata = data['metadata']
                if 'item' in data:
                    print("collecting %s..." % id)
                    record = {'identifier': jdata['identifier'][0], 
                        'upload_date': jdata['addeddate'][0],
                        'total_views': data['item']['downloads'],
                        'title': jdata['title'][0],
                        'topic': "; ".join(jdata['subject']),
                        'collection': "; ".join(jdata['collection'])
                        }
                    writer.writerow(record)
                    print("writing %s..." % id)
                else:
                    print("collecting %s with no downloads..." % id) 
                    alt_record = {'identifier': jdata['identifier'][0], 
                        'upload_date': jdata['addeddate'][0],
                        'total_views': "0",
                        'title': jdata['title'][0],
                        'topic': "; ".join(jdata['subject']),
                        'collection': "; ".join(jdata['collection'])
                        }
                    writer.writerow(alt_record)
                    print("writing %s..." % id)
            except urllib.error.HTTPError as e:
                print("identifer %s has exception: %s..." % (id, e))
                missing_record = {'identifier': id,
                    'upload_date': "",
                    'total_views': "",
                    'title': e,
                    'topic': "",
                    'collection': ""
                    }
                writer.writerow(missing_record)
            except:
                print("collecting %s with no subject..." % id)
                broken_record = {'identifier': jdata['identifier'][0],
                    'upload_date': jdata['addeddate'][0],
                    'total_views': data['item']['downloads'],
                    'title': jdata['title'][0], 
                    'topic': "0 -- subject is missing",
                    'collection': "; ".join(jdata['collection'])
                    }
                writer.writerow(broken_record)
                print("writing %s..." % id)
                
print('%s %s' % ('Done @', datetime.now()))