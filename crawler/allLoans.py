import json
from models import Loan
import datetime
import sys, getopt, os
import csv 
import argparse

from common import loan_features
from common import log
from common import forwardRequest
from common import loan_page
from common import loan_each
from common import loan_lender_page
from common import loan_team_page
from common import readLoanIdsToDict
from common import readDicValuesFromCsv
from bs4 import BeautifulSoup
'''

read inputs

'''
parser = argparse.ArgumentParser()
parser.add_argument("-o", dest="output_dir",
                    help="directory for output files")
args = parser.parse_args()



output_dir = args.output_dir

loan_csv = os.path.join(output_dir,'loan.csv')
loan_id_csv = os.path.join(output_dir,'loan_id.csv')
loan_lender_csv = os.path.join(output_dir,'loan_lender.csv')
loan_team_csv = os.path.join(output_dir,'loan_team.csv')

if not os.path.exists(output_dir):
    os.makedirs(output_dir)


loan_ids = []
loan_lenders = {}
loan_teams = {}

'''
Writing column names
'''
with open(loan_csv, 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(loan_features)



with open(loan_id_csv, 'a+') as outfile:
    writer = csv.writer(outfile)
    for n in range(14000):
        pageid=str(n*100)
        site= 'https://api.kivaws.org/v2/loans?limit=10&facets=true&type=lite&sortBy=newest&offset='+pageid+'&q=j:{"status":"all"}'
        response = forwardRequest(site,'crawling the page: '+str(pageid))
        this_page = json.loads(response.read())
        for record in this_page['entities']:
            loan_ids.append(record['properties']['id'])
            writer.writerow([record['properties']['id']])


'''
crawling loans' lenders and teams
'''


for i in range(len(loan_ids)):
    loan_lenders[loan_ids[i]]=[]
    try:
        total_pages = json.loads(forwardRequest(loan_lender_page(loan_ids[i],1),'crawling the '+str(i+1)+' loan lenders for loan id '+str(loan_ids[i])).read())['paging']['pages']
    except Exception as e:
        print str(e)
        continue
    for j in range(total_pages):
        try:
            response = forwardRequest(loan_lender_page(loan_ids[i],j+1),'crawling the '+str(i+1)+' loan lenders: page '+str(j+1)+', '+' out of '+str(total_pages)+' pages for loan '+str(loan_ids[i])+' out of '+str(len(loan_ids))+' loans')
        except Exception as e:
            print str(e)
            continue
        this_page = json.loads(response.read())
        page_size = len(this_page['lenders'])
        for k in range(page_size):
            if 'lender_id' not in this_page['lenders'][k]:
                loan_lenders[loan_ids[i]].append('anonymous')
            elif this_page['lenders'][k]['lender_id'] not in loan_lenders[loan_ids[i]]:
                loan_lenders[loan_ids[i]].append(this_page['lenders'][k]['lender_id'])

with open(loan_lender_csv, 'wb') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in loan_lenders.items():
       writer.writerow([key, value])



for i in range(len(loan_ids)):
    loan_teams[loan_ids[i]]=[]
    try:
        total_pages = json.loads(forwardRequest(loan_team_page(loan_ids[i],1),'crawling the '+str(i+1)+' loan teams for loan id '+str(loan_ids[i])).read())['paging']['pages']
    except Exception as e:
        print str(e)
        continue
    for j in range(total_pages):
        try:
            response = forwardRequest(loan_team_page(loan_ids[i],j+1),'crawling the '+str(i+1)+' loan teams: page '+str(j+1)+', '+' out of '+str(total_pages)+' pages for loan '+str(loan_ids[i])+' out of '+str(len(loan_ids))+' loans')
        except Exception as e:
            print str(e)
            continue
        this_page = json.loads(response.read())
        page_size = len(this_page['teams'])
        for k in range(page_size):
            if this_page['teams'][k]['id'] not in loan_teams[loan_ids[i]]:
                loan_teams[loan_ids[i]].append(this_page['teams'][k]['id'])

with open(loan_team_csv, 'wb') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in loan_teams.items():
       writer.writerow([key, value])

'''
crawling loans
'''


for i in range(len(loan_ids)):
    _loan_id = loan_ids[i]
    try:
        response = forwardRequest(loan_each(_loan_id),'crawling the '+str(i+1)+' loan: '+str(_loan_id)+', '+' out of '+str(len(loan_ids)))
    except Exception as e:
        print str(e)
        continue
    _loan_json = json.loads(response.read())['loans'][0]
    for k in loan_features:
        if k not in _loan_json.keys():
            _loan_json[k] = 'N/A'
    _loan = Loan(_loan_json)
    _loan.write(loan_csv, loan_features)




