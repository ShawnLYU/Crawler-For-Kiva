import urllib2
import json
from models import Lender
import ast
import sys, getopt, os
import csv 
import ast
from common import lender_features
from common import lender_each
from common import forwardRequest


opts, args = getopt.getopt(sys.argv[1:],"i:o:")


def help():
    print
    '''
    -i  dir for lender ids
    -o  output output_dir
    '''


    sys.exit()


for opt, arg in opts:
    if opt == '-o':
        output_dir = arg
    elif opt == '-i':
        lender_id_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),arg,'loan_lender.csv')

with open(lender_id_dir, 'rb') as csv_file:
    reader = csv.reader(csv_file)
    mydict = dict(reader)

total_lenders_tmp=[ast.literal_eval(mydict[e]) for e in mydict]
total_lenders = set([item for sublist in total_lenders for item in sublist])

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
        response = forwardRequest(lender_each(_lender_id),'crawling the lender: '+str(_lender_id)+', '+' out of '+str(len(total_lenders))+' lenders ')
        _lender_json = json.loads(response.read())['lenders'][0]
        for k in lender_features:
            if k not in _lender_json.keys():
                _lender_json[k] = 'N/A'
    _lender = Lender(_lender_json)
    _lender.write(lender_csv, lender_features)





