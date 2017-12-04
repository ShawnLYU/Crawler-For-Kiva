import urllib2
import json
from models import Partner
import ast
import sys, getopt, os
import csv 
import ast
import argparse
from common import partner_features
from common import partner_page
from common import forwardRequest
parser = argparse.ArgumentParser()
parser.add_argument("-o", dest="output_dir",
                    help="directory for output files")

args = parser.parse_args()

    

partner_csv = os.path.join(os.path.abspath(args.output_dir),'partner.csv')

with open(partner_csv, 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(partner_features)

total_pages = json.loads(forwardRequest(partner_page(1),'crawling the number of total pages for partners').read())['paging']['pages']
for i in range(1, total_pages+1):
    response = forwardRequest(partner_page(i),'crawling the partners: page '+str(i)+', '+' out of '+str(total_pages)+' pages')
    this_page = json.loads(response.read())
    page_size = len(this_page['partners'])

    for j in range(page_size):
        _partner_json = this_page['partners'][j]
        for k in partner_features:
            if k not in _partner_json.keys():
                _partner_json[k] = 'N/A'
        _partner = Partner(_partner_json)
        _partner.write(partner_csv, partner_features)


