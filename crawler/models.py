import csv
'''

define write() for each model

'''

class Loan:
    def __init__(self, loan_info):
        self.loan_info = loan_info



    def write(self, file_path, feature):
        with open(file_path, 'a+') as outfile:
            writer = csv.writer(outfile)
            writer.writerow([unicode(self.loan_info[f]).encode("utf-8").replace("\n", "\\n") for f in feature])
 

class Lender:
    def __init__(self, lender_info):
        self.lender_info = lender_info

    def write(self, file_path, feature):
        with open(file_path, 'a+') as outfile:
            writer = csv.writer(outfile)
            writer.writerow([unicode(self.lender_info[f]).encode("utf-8").replace("\n", "\\n") for f in feature])
 


class Partner:
    def __init__(self, partner_info):
        self.partner_info = partner_info

    def write(self, file_path, feature):
        with open(file_path, 'a+') as outfile:
            writer = csv.writer(outfile)
            writer.writerow([unicode(self.partner_info[f]).encode("utf-8").replace("\n", "\\n") for f in feature])
 



class Team:
    def __init__(self, team_info):
        self.team_info = team_info

    def write(self, file_path, feature):
        with open(file_path, 'a+') as outfile:
            writer = csv.writer(outfile)
            writer.writerow([unicode(self.team_info[f]).encode("utf-8").replace("\n", "").replace("\r", "") for f in feature])
 


class Teammember:
    def __init__(self, teammember_info):
        self.teammember_info = teammember_info

    def write(self, file_path, feature):
        with open(file_path, 'a+') as outfile:
            writer = csv.writer(outfile)
            writer.writerow([unicode(self.teammember_info[f]).encode("utf-8").replace("\n", "\\n") for f in feature])
 
