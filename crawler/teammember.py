import urllib2
import json
from models import Team
import ast
import sys, getopt, os
import csv 
import ast

from common import teammember_page
from common import teammember_features
from common import forwardRequest
opts, args = getopt.getopt(sys.argv[1:],"i:o:")

def help():
    print
    '''
    -i  dir for loan ids
    -o  output output_dir
    '''


    sys.exit()


for opt, arg in opts:
    if opt == '-o':
        output_dir = arg
    elif opt == '-i':
        team_id_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),arg,'loan_id.csv')

with open(team_id_dir, 'rb') as csv_file:
    reader = csv.reader(csv_file)
    mydict = dict(reader)

total_teams_tmp=[ast.literal_eval(mydict[e]) for e in mydict]
total_teams = set([item for sublist in total_teams_tmp for item in sublist])

team_member_csv = os.path.join(output_dir,'team_member.csv')


if not os.path.exists(output_dir):
    os.makedirs(output_dir)


with open(team_member_csv, 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(partner_features)

total_pages = json.loads(forwardRequest(teammember_page(1),'crawling the number of total pages for teammembers').read())['paging']['pages']
for i in range(1, total_pages+1):
    response = forwardRequest(partner_page(i),'crawling the team: page '+str(i)+', '+' out of '+str(total_pages)+' pages')
    this_page = json.loads(response.read())
    page_size = len(this_page['lenders'])

    for j in range(page_size):
        _teammember_json = this_page['lenders'][j]
        for k in teammember_features:
            if k not in _teammember_json.keys():
                _teammember_json[k] = 'N/A'
        _teammember = Teammember(_teammember_json)
        _partner.write(team_member_csv, teammember_features)





