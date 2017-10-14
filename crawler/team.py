import urllib2
import json
from models import Team
import ast
import sys, getopt, os
import csv 
import ast
from common import team_features
from common import team_each
from common import forwardRequest
opts, args = getopt.getopt(sys.argv[1:],"i:o:")

def help():
    print
    '''
    -i  dir for team ids
    -o  output output_dir
    '''


    sys.exit()


for opt, arg in opts:
    if opt == '-o':
        output_dir = os.path.abspath(arg)
    elif opt == '-i':
        team_id_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),arg,'loan_team.csv')

with open(team_id_dir, 'rb') as csv_file:
    reader = csv.reader(csv_file)
    mydict = dict(reader)

total_teams_tmp=[ast.literal_eval(mydict[e]) for e in mydict]
total_teams = set([item for sublist in total_teams_tmp for item in sublist])


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
    response = forwardRequest(team_each(_team_id),'crawling the team: '+str(_team_id)+', '+' out of '+str(len(total_teams))+' teams ')
    _team_json = json.loads(response.read())['teams'][0]
    for k in team_features:
        if k not in _team_json.keys():
            _team_json[k] = 'N/A'
    _team = Team(_team_json)
    _team.write(team_csv, team_features)








