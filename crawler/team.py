import urllib2
import json
from models import Team
import ast
import sys, getopt, os
import csv 
import ast
import argparse
from common import team_features
from common import team_each
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

team_csv = os.path.join(output_dir,'team.csv')


if not os.path.exists(output_dir):
    os.makedirs(output_dir)


'''

parameter definitions for further reference

'''




'''
Writing column names
'''

with open(team_csv, 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(team_features)



for i in range(len(total_teams)):
    _team_id = total_teams[i]
    try:
        response = forwardRequest(team_each(_team_id),'crawling the '+str(i+1)+' team: '+str(_team_id)+', '+' out of '+str(len(total_teams))+' teams ')
    except Exception as e:
        print str(e)
        continue
    _team_json = json.loads(response.read())['teams'][0]
    for k in team_features:
        if k not in _team_json.keys():
            _team_json[k] = 'N/A'
    _team = Team(_team_json)
    _team.write(team_csv, team_features)








