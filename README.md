pre_folder=11-05
folder=11-06


# first time run this, without previous input
python loan.py -o $folder
# crawl with previous 
python loan.py -i $pre_folder -o $folder
# rearrange additional information
python loan_additional_info.py -i $folder -o $folder
python lender.py -i $folder -o $folder 
python team.py -i $folder -o $folder
python teammember.py -i $folder -o $folder

# collect all teams and loans
python allteams.py -o ./all
python allLoans.py -o ./all