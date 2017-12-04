import urllib2
import json
from models import Teammember
import ast
import sys, getopt, os
import csv 
import ast
import argparse

from common import teammember_page
from common import teammember_features
from common import forwardRequest
from common import readDicValuesFromCsv


parser = argparse.ArgumentParser()
parser.add_argument("-o", dest="output_dir",
                    help="directory for output files")
parser.add_argument("-i", dest="input_dir",
                    help="loan team relation file directory")
args = parser.parse_args()



output_dir = os.path.abspath(args.output_dir)
total_teams = readDicValuesFromCsv(os.path.join(os.path.dirname(os.path.abspath(__file__)),args.input_dir,'loan_team.csv'))

team_member_csv = os.path.join(output_dir,'team_member.csv')


if not os.path.exists(output_dir):
    os.makedirs(output_dir)


with open(team_member_csv, 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(teammember_features)


for _team_id_index in range(len(total_teams)):
    try:
        total_pages = json.loads(forwardRequest(teammember_page(total_teams[_team_id_index],1),'crawling the number of total pages for teammembers of team '+str(_team_id_index+1)+' out of '+str(len(total_teams))+' teams').read())['paging']['pages']
    except Exception as e:
        print str(e)
        continue
    for i in range(1, total_pages+1):
        try:
            response = forwardRequest(teammember_page(total_teams[_team_id_index],i),'crawling the team: page '+str(i)+', '+' out of '+str(total_pages)+' pages for team '+str(_team_id_index))
        except Exception as e:
            print str(e)
            continue
        this_page = json.loads(response.read())
        page_size = len(this_page['lenders'])
        for j in range(page_size):
            _teammember_json = this_page['lenders'][j]
            _teammember_json['team_id'] = total_teams[_team_id_index]
            for k in teammember_features:
                if k not in _teammember_json.keys():
                    _teammember_json[k] = 'N/A'
            _teammember = Teammember(_teammember_json)
            _teammember.write(team_member_csv, teammember_features)





