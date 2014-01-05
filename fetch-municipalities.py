#!/usr/bin/env python

"""
This tool fetches the list of municipalities from Statistics Finland,
generates the IDs according to OCD (http://opencivicdata.org/) guidelines,
and outputs the data into a CSV file.
"""

import re
import requests
import requests_cache
import unicodecsv

import csv

requests_cache.install_cache('municipalities')

SOURCE_URL = 'http://www.tilastokeskus.fi/meta/luokitukset/kunta/001-2014/tekstitiedosto.txt'
SOURCE_CHARSET = 'iso8859-1'

def fetch_munis():
    resp = requests.get(SOURCE_URL)
    s = resp.content.decode(SOURCE_CHARSET)
    lines = s.splitlines()
    # Remove lines until we get to the actual data.
    while not re.match('\d+\t', lines[0]):
        lines.pop(0)

    munis = []
    for line in lines:
        (muni_id, muni_name) = line.split('\t')
        print(muni_name)
        ocd_name = muni_name.lower()
        if '-' in ocd_name: # Maarianhamina - Mariehamn
            ocd_name = ocd_name.split('-')[0].strip()
        ocd_name = ocd_name.replace(' ', '_')
        ocd_id = "ocd-division/country:fi/kunta:%s" % ocd_name
        munis.append((muni_id, ocd_id, muni_name))
    return munis

def output_munis(munis):
    f = open('kunnat.csv', 'w')
    writer = unicodecsv.writer(f, encoding='utf-8')
    for muni in munis:
        writer.writerow((muni[1], muni[2]))

munis = fetch_munis()
output_munis(munis)
