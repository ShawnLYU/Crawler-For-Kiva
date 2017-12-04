from datetime import datetime
import time, os
import urllib2
import ast, csv

loan_features = [
    'id',
    'name',
    'description',
    'status',
    'funded_amount',
    'basket_amount',
    'image',
    'activity',
    'sector',
    'themes',
    'use',
    'location',
    'partner_id',
    'posted_date',
    'planned_expiration_date',
    'loan_amount',
    'lender_counter',
    'bonus_credit_eligibility',
    'tags',
    'borrowers',
    'terms',
    'payments',
    'journal_totals',
]

lender_features = [
    'lender_id',
    'name',
    'image',
    'whereabouts',
    'country_code',
    'uid',
    'member_since',
    'personal_url',
    'occupation',
    'loan_because',
    'occupational_info',
    'loan_count',
    'invitee_count',
]

team_features = [
        "id",
        "shortname",
        "name",
        "category",
        "image",
        "whereabouts",
        "loan_because",
        "description",
        "website_url",
        "team_since",
        "membership_type",
        "member_count",
        "loan_count",
        "loaned_amount",
]

partner_features = [
         "id",
         "name",
         "status",
         "rating",
         "image",
         "start_date",
         "countries",
         "delinquency_rate",
         "default_rate",
         "total_amount_raised",
         "loans_posted",
         "delinquency_rate_note",
         "default_rate_note",
         "portfolio_yield_note",
         "charges_fees_and_interest",
         "average_loan_size_percent_per_capita_income",
         "loans_at_risk_rate",
         "currency_exchange_loss_rate",
]


teammember_features = [
    "lender_id",
    "name",
    "image",
    "whereabouts",
    "country_code",
    "uid",
    "team_join_date",
    "team_id",
]
'''

forward request with speed limitations

'''
def forwardRequest(link,logInfo=''):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(link,headers=hdr)
    response = urllib2.urlopen(req)
    remaining = response.info().getheader('X-RateLimit-Overall-Remaining')
    log(logInfo+' | ratelimit specific remaining: '+str(remaining))
    try:
        rateMonitor(remaining)
    except Exception as e:
        log('No monitoring excuted')
    return response

def rateMonitor(remaining):
    if int(remaining) <= 2:
        log('X-RateLimit-Overall-Remaining reaches maximum, too tired, I need to take a minute break :)')
        time.sleep(61)


def log(info):
    print datetime.now().strftime('%m-%d %H:%M:%S'),info

'''

accessing API functions

'''
def loan_page(no):
    return "https://api.kivaws.org/v1/loans/newest.json?page=%d" % (no)

def partner_page(no):
    return "https://api.kivaws.org/v1/partners.json?page=%d" % (no)

def loan_each(no):
    no = str(no)
    return "https://api.kivaws.org/v1/loans/%s.json" % (no)

def loan_lender_page(loanid,page):
    loanid = str(loanid)
    return "http://api.kivaws.org/v1/loans/%s/lenders.json?page=%d" % (loanid,page) 

def loan_team_page(teamid,page):
    teamid = str(teamid)
    return "http://api.kivaws.org/v1/loans/%s/teams.json?page=%d" % (teamid,page)   

def lender_each(lenderid):
    lenderid = str(lenderid)
    return "https://api.kivaws.org/v1/lenders/%s.json" % (lenderid)   

def team_each(teamid):
    teamid = str(teamid)
    return "https://api.kivaws.org/v1/teams/%s.json" % (teamid) 

def teammember_page(teamid,page):
    teamid = str(teamid)
    return "https://api.kivaws.org/v1/teams/%s/lenders.json?page=%d" % (teamid,page)




'''
supplementary functions 

'''
def readDicValuesFromCsv(filePath):
    with open(filePath, 'rb') as csv_file:
        reader = csv.reader(csv_file)
        mydict = dict(reader)
    ids=[]
    for v in mydict.values():
        ids+=ast.literal_eval(v)
    return list(set(ids))


def readLoanIdsToDict(filePath):
    with open(filePath, 'rb') as csv_file:
        reader = csv.reader(csv_file)
        mydict = dict(reader)
    return mydict








