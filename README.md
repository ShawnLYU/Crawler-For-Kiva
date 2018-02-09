## This package is implemented to crawl loans related data from **Kiva**
### About Kiva
>Kiva is an international nonprofit, founded in 2005 and based in San Francisco, with a mission to connect people through lending to alleviate poverty. We celebrate and support people looking to create a better future for themselves, their families and their communities.

Description about Kiva could be found via https://www.kiva.org

### Usage

 - pre_folder=11-05
 - folder=11-06

#### To crawl loans and related information on daily-base

###### first time run this, without previous input
python loan.py -o $folder
###### crawl with previous 
python loan.py -i $pre_folder -o $folder
###### rearrange additional information
 - python loan_additional_info.py -i $folder -o $folder
 - python lender.py -i $folder -o $folder 
 - python team.py -i $folder -o $folder
 - python teammember.py -i $folder -o $folder

#### To crawl all loans and related information (this could be time consuming and ip-pool should be provided)

###### collect all teams and loans
 - python allteams.py -o ./all
 - python allLoans.py -o ./all
