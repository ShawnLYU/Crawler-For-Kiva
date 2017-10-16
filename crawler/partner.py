import urllib2
import json
from models import Partner
import ast
import sys, getopt, os
import csv 
import ast
from common import partner_features
from common import partner_page
from common import forwardRequest

opts, args = getopt.getopt(sys.argv[1:],"o:h")

def help():
    print '''
    -o out_dir
    python partner.py -o >> 2>&1 &
    '''
    sys.exit()


for opt, arg in opts:
    if opt == '-o':
        output_dir = os.path.abspath(arg)
    elif opt == '-h':
        help()

    

partner_csv = os.path.join(output_dir,'partner.csv')

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


