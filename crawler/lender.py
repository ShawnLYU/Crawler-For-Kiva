import urllib2
import json
from models import Lender
import ast
import sys, getopt, os
import csv 
import ast
import argparse
from common import lender_features
from common import lender_each
from common import forwardRequest
from common import readDicValuesFromCsv

'''

read inputs

'''
parser = argparse.ArgumentParser()
parser.add_argument("-o", dest="output_dir",
                    help="directory for output files")
parser.add_argument("-i", dest="input_dir",
                    help="loan lender relation file directory")
args = parser.parse_args()

output_dir = os.path.abspath(args.output_dir)
total_lenders = readDicValuesFromCsv(os.path.join(os.path.dirname(os.path.abspath(__file__)),args.input_dir,'loan_lender.csv'))
lender_csv = os.path.join(output_dir,'lender.csv')


if not os.path.exists(output_dir):
    os.makedirs(output_dir)


'''
Writing column names
'''

with open(lender_csv, 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(lender_features)


'''
crawling lenders
'''


for i in range(len(total_lenders)):
    _lender_id = total_lenders[i]
    if _lender_id != 'anonymous':
        try:
            response = forwardRequest(lender_each(_lender_id),'crawling the '+str(i+1)+' lender: '+str(_lender_id)+', '+' out of '+str(len(total_lenders))+' lenders ')
            _lender_json = json.loads(response.read())['lenders'][0]
        except Exception as e:
            print lender_each(_lender_id),'crawling the '+str(i+1)+' lender: '+str(_lender_id)+', '+' out of '+str(len(total_lenders))+' lenders '
            print str(e)
            _lender_json={}
        for k in lender_features:
            # in case there are some features that are not stored previously
            if k not in _lender_json.keys():
                _lender_json[k] = 'N/A'
    _lender = Lender(_lender_json)
    _lender.write(lender_csv, lender_features)






