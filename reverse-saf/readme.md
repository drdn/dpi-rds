# reverse-saf

A script to reverse all the hard work performed on DSpace records. Using a list of handles, this script will create a *reverse simple archive format* (well, not quite) package for the purpose of downloading metadata and bitstreams for DSpace records.
This script is necessary to create a set of 'test datasets' for populating various repository platforms during the pilot stage.

## Usage

`python3 reverse-saf.py <handle-list.txt>`

## Nota bene

This script contains a prebuilt query for DRUM using the OAI-PMH protocol. This script is also missing certain useful features such as XML to CSV conversion for metadata records, checksum validation, destination directory argument, and user input to confirm downloads of bitstreams in excess of 2GB. *You've been warned.*
