import json
from models import Loan

import sys, getopt, os
import csv 

from common import loan_features
from common import log
from common import forwardRequest
from common import loan_page
from common import loan_each
from common import loan_lender_page
from common import loan_team_page


opts, args = getopt.getopt(sys.argv[1:],"o:")

def help():
    print
    '''
    -o  output output_dir
    '''


    sys.exit()


for opt, arg in opts:
    if opt == '-o':
        output_dir = os.path.abspath(arg)



loan_csv = os.path.join(output_dir,'loan.csv')
loan_id_csv = os.path.join(output_dir,'loan_id.csv')
loan_lender_csv = os.path.join(output_dir,'loan_lender.csv')
loan_team_csv = os.path.join(output_dir,'loan_team.csv')

if not os.path.exists(output_dir):
    os.makedirs(output_dir)



loan_ids = []
loan_lenders={}
loan_teams={}


'''
Writing column names
'''
with open(loan_csv, 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(loan_features)



'''
crawling loan ids
'''




total_pages = json.loads(forwardRequest(loan_page(1),'crawling the number of total pages').read())['paging']['pages']
for i in range(1, total_pages+1):
    response = forwardRequest(loan_page(i),'crawling the loan ids: page '+str(i)+', '+' out of '+str(total_pages)+' pages')
    this_page = json.loads(response.read())
    page_size = len(this_page['loans'])
    for j in range(page_size):
        if this_page['loans'][j]['id'] not in loan_ids:
            loan_ids.append(this_page['loans'][j]['id'])
'''
save loan ids to file
'''
with open(loan_id_csv, 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(loan_ids)



'''
crawling loans' lenders and teams
'''


for i in range(len(loan_ids)):
    loan_lenders[loan_ids[i]]=[]

    total_page = json.loads(forwardRequest(loan_lender_page(loan_ids[i],1),'crawling the lender for loan id '+str(loan_ids[i])).read())['paging']['pages']
    for j in range(total_page):
        response = forwardRequest(loan_lender_page(loan_ids[i],j+1),'crawling the loan lenders: page '+str(j)+', '+' out of '+str(total_pages)+' pages for loan '+str(loan_ids[i]))
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
    total_page = json.loads(forwardRequest(loan_team_page(loan_ids[i],1)).read(),'crawling the team for loan id '+str(loan_ids[i]))['paging']['pages']
    for j in range(total_page):
        response = forwardRequest(loan_team_page(loan_ids[i],j+1),'crawling the loan teams: page '+str(j)+', '+' out of '+str(total_pages)+' pages for loan '+str(loan_ids[i]))
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
    time.sleep(1.1)
    _loan_id = loan_ids[i]
    response = forwardRequest(loans_each(_loan_id),'crawling the loan: '+str(_loan_id)+', '+' out of '+str(len(loan_ids)))
    _loan_json = json.loads(response.read())['loans'][0]
    for k in loan_features:
        if k not in _loan_json.keys():
            _loan_json[k] = 'N/A'
    _loan = Loan(_loan_json)
    _loan.write(loan_csv, loan_features)




