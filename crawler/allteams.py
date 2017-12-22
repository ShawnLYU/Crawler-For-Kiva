import sys,os
from bs4 import BeautifulSoup
import urllib,urllib2  
from models import Team
import json
import re

import csv 
import argparse
from common import forwardRequest
from common import readDicValuesFromCsv
from common import team_features
from common import team_each_shortname

parser = argparse.ArgumentParser()
parser.add_argument("-o", dest="output_dir", required=True,
                    help="directory for output files")
args = parser.parse_args()



output_dir = args.output_dir
output_file = os.path.join(output_dir,'all_teams.csv')
team_all_csv = os.path.join(output_dir,'team_all.csv')


if not os.path.exists(output_dir):
    os.makedirs(output_dir)



with open(output_file, 'a+') as outfile:
    writer = csv.writer(outfile)
    teamnames = []
    for pageid in range(10000):
        site= "https://www.kiva.org/teams?pageID="+str(pageid)
        page = forwardRequest(site,'crawling the page: '+str(pageid))
        soup = BeautifulSoup(page)
        if len(soup.find_all("a", { "class":"img img-s135 thumb " },href=True)) == 0:
            break
        for link in soup.find_all("a", { "class":"img img-s135 thumb " },href=True):
            teamnames.append(link['href'].split('/')[-1])
    writer.writerow(teamnames)



with open(team_all_csv, 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(team_features)

for i in range(len(teamnames)):
    _team_name = teamnames[i]
    try:
        response = forwardRequest(team_each_shortname(_team_name),'crawling the '+str(i+1)+' team: '+teamnames[i]+', '+' out of '+str(len(teamnames))+' teams ')
    except Exception as e:
        print str(e)
        continue
    _team_json = json.loads(response.read())['teams'][0]
    for k in team_features:
        if k not in _team_json.keys():
            _team_json[k] = 'N/A'
    _team = Team(_team_json)
    _team.write(team_all_csv, team_features)























