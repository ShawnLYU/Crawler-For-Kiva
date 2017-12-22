import sys,os
from bs4 import BeautifulSoup
import urllib,urllib2  

import json
import re

import csv 
import argparse
from common import forwardRequest
from common import readDicValuesFromCsv

parser = argparse.ArgumentParser()
parser.add_argument("-o", dest="output_dir", required=True,
                    help="directory for output files")
parser.add_argument("-i", dest='input_dir', required=True,
                    help="if previous loan id exists, please provide it as id pool to accumulate")
args = parser.parse_args()



output_dir = args.output_dir
prev_id_dir = args.input_dir
loan_additional_info = os.path.join(output_dir,'loan_additional_info.csv')
loan_additional_info_view = os.path.join(output_dir,'loan_additional_info_view.csv')


if not os.path.exists(output_dir):
    os.makedirs(output_dir)


loan_ids = readDicValuesFromCsv(os.path.join(prev_id_dir,'loan_id.csv')) if prev_id_dir else {}
with open(loan_additional_info, 'a+') as outfile:
    writer = csv.writer(outfile)
    counter = 0
    for loan_id in loan_ids:
        counter += 1
        site= "https://www.kiva.org/lend/"+str(loan_id)

        page = forwardRequest(site,'crawling the loan ids: '+str(counter)+', '+' out of '+str(len(loan_ids))+' loans')
        soup = BeautifulSoup(page)
        try:
            funded_percentage = soup.find_all("h2", { "class" : "green-bolded inline" })[0].contents[0].strip()

            # team and lender information
            # using regex extract needed information
            pattern = re.compile(r"view_data\s*:\s*(\{.*?\})\n")
            script = soup.find("script", text=pattern)

            data = pattern.search(script.text).group(1)

            writer.writerow([loan_id,funded_percentage,str(data)])
        except Exception as e:
            print str(e)
            writer.writerow([loan_id,'N/A','N/A'])
            continue



with open(loan_additional_info, 'rb') as f:
    reader = csv.reader(f)
    your_list = list(reader)

import json
# your_list is a list of informtion, the second of which contains a json that could be converted to a dictionary
keys = json.loads(your_list[0][2]).keys()
with open(loan_additional_info_view, 'a+') as outfile:
    writer = csv.writer(outfile)
    header = ['id','status']+keys
    writer.writerow(header)
    for row in your_list:
        _this_row = [your_list[0][0],your_list[0][1]]
        _this_dic = json.loads(row[2])
        for k in keys:
            try:
                _this_row.append(_this_dic[k])
            except Exception as s:
                _this_row.append('')
        writer.writerow(_this_row)




















