import requests
import json
import argparse
import csv
import os
from email.utils import parseaddr
from datetime import datetime
from breach_data import breach_data

parser = argparse.ArgumentParser("dehasheddumper.py")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--domain", metavar='<domain>', help="Domain name to extract leaks", type=str, required=False)
group.add_argument("--domains", metavar='<file>', help="Newline separated file with domain names", required=False)
parser.add_argument("--email", metavar='<email>', help="Dehashed email account", type=str, required=False)
parser.add_argument("--api-token", metavar='<token>', help="Dehashed API token", type=str, required=False)
parser.add_argument("--full", help="Dump all data from Dehashed into CSV", required=False, action='store_true')

args = parser.parse_args()

class bcolors:
    OK = '\033[92m'
    INFO = '\033[94m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

print("""\

▓█████▄ ▓█████▄  █    ██  ███▄ ▄███▓ ██▓███  ▓█████  ██▀███  
▒██▀ ██▌▒██▀ ██▌ ██  ▓██▒▓██▒▀█▀ ██▒▓██░  ██▒▓█   ▀ ▓██ ▒ ██▒
░██   █▌░██   █▌▓██  ▒██░▓██    ▓██░▓██░ ██▓▒▒███   ▓██ ░▄█ ▒
░▓█▄   ▌░▓█▄   ▌▓▓█  ░██░▒██    ▒██ ▒██▄█▓▒ ▒▒▓█  ▄ ▒██▀▀█▄  
░▒████▓ ░▒████▓ ▒▒█████▓ ▒██▒   ░██▒▒██▒ ░  ░░▒████▒░██▓ ▒██▒
 ▒▒▓  ▒  ▒▒▓  ▒ ░▒▓▒ ▒ ▒ ░ ▒░   ░  ░▒▓▒░ ░  ░░░ ▒░ ░░ ▒▓ ░▒▓░
 ░ ▒  ▒  ░ ▒  ▒ ░░▒░ ░ ░ ░  ░      ░░▒ ░      ░ ░  ░  ░▒ ░ ▒░
 ░ ░  ░  ░ ░  ░  ░░░ ░ ░ ░      ░   ░░          ░     ░░   ░ 
   ░       ░       ░            ░               ░  ░   ░     
 ░       ░                                         ░ by LRVT                  
""")
print()

# hardcoded credentials
dehashed_user="<email>"
dehashed_apikey="<api-token>"

date = datetime.now().strftime("%Y%m%d-%H%M")
balance = 0
script_dir = os.path.dirname(__file__)
try:
	# create subdir results
	os.mkdir(os.path.join(script_dir, "results/"))
except:
	pass
checkAPI = True

if (args.email):
	dehashed_user = args.email
if (args.api_token):
	dehashed_apikey = args.api_token

if (args.domains):
	f = open(args.domains)
	domains = f.read().split("\n")
	f.close()
else:
	domains = args.domain.split("\n")

domains = list(filter(None, domains))

for domain in domains:
	domain = domain.strip().strip('www.')
	url = 'https://api.dehashed.com/search'
	params={'query':'email:'+domain,'size':'10000'}

	headers = {
	    "Host": "api.dehashed.com",
	    "Connection": "keep-alive",
	    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
	    "Accept": "application/json"
	}

	try:
		# only print API access testing once
		if checkAPI:
			print("[~] Verifying Dehashed API credentials. Please wait...")
		response = requests.get(url, params=params, headers=headers, auth=(dehashed_user, dehashed_apikey))
		data = response.json()

		# if API does not respond with status code 200
		if (response.status_code != 200):
			print(bcolors.FAIL + "[x]" + bcolors.ENDC + " Status " + str(response.status_code) + " - Dehashed down or invalid API credentials.")
			exit()
		else:
			# only print API access testing once
			if checkAPI:
				print(bcolors.OK + "[✓]" + bcolors.ENDC + " Successful API authentication. Let's go looting..." + bcolors.ENDC)
				checkAPI = False
			balance = data['balance']
			print()

		print("[~] Performing leak check on " + str(domain))

		# if there are no leaks available
		if (data['total'] == 0):
			print(bcolors.WARNING + "[✓]" + bcolors.ENDC + " Finished leak check on " + str(domain) + bcolors.ENDC)
			print("    > No leaks available.")
			continue

		if(args.full):
			alldata_filename = os.path.join(script_dir, "results/" + str(date) + "_DD_" + str(domain) + "_fulldata.csv")
			alldata_file = csv.writer(open(alldata_filename, "a"))
			alldata_file.writerow(["Leak ID", "Domain", "Email", "Username", "Password", "Password_Hash", "Name", "VIN", "Address", "IP Address", "Phone", "Breach", "Description", "Date", "Leak Count", "Leak Type"])
			
		# file containing user email addresses
		user_file_name = os.path.join(script_dir, "results/" + str(date) + "_DD_" + str(domain) + "_users.lst")
		user_file = open(user_file_name, "w")
		# file containing leaked user passwords
		password_file_name = os.path.join(script_dir, "results/" + str(date) + "_DD_" + str(domain) + "_passwords.lst")
		password_file = open(password_file_name, "w")

		# list to store user emails
		users = []
		# list to store user passwords
		passwords = [] 

		for leak in data['entries']:
			if ("@"+domain in parseaddr(str(leak['email']))[1]):
				identifier=str(leak['id'])
				email=parseaddr(str(leak['email']))[1]
				username=str(leak['username'])
				password=str(leak['password'])
				hashed_password=str(leak['hashed_password'])
				name=str(leak['name'])
				vin=str(leak['vin'])
				address=str(leak['address'])
				ip_address=str(leak['ip_address'])
				phone=str(leak['phone'])
				breach=str(leak['database_name'])

				# add user email to list
				users.append(str(email))
				# add leaked pw to list
				passwords.append(str(password))

				# dump all leak data into a csv file
				if(args.full):
					alldata_filename = os.path.join(script_dir, "results/" + str(date) + "_DD_" + str(domain) + "_fulldata.csv")
					alldata_file = csv.writer(open(alldata_filename, "w"))
					breach_desc = ""
					breach_date = ""
					breach_leakcount = ""
					breach_leaktypes = ""

					# if the breach comes from Cit0day
					if "Cit0day" in breach:
						# find index of breach with name Cit0day
						cit0day_index = next((index for (index, d) in enumerate(breach_data) if d["name"] == "Cit0day"), None)
						breach_desc = breach_data[cit0day_index]['description']
						breach_date = breach_data[cit0day_index]['date']
						breach_leakcount = breach_data[cit0day_index]['leakcount']
						breach_leaktypes = breach_data[cit0day_index]['leaktypes']
					else:
						# if not from Cit0day, then loop thorugh the breach dataset
						for leakentry in breach_data:
							if leakentry['name'] == breach:
								breach_desc = leakentry['description']
								breach_date = leakentry['date']
								breach_leakcount = leakentry['leakcount']
								breach_leaktypes = leakentry['leaktypes']

					alldata_file.writerow([identifier, domain, email, username, password, hashed_password, name, vin, address, ip_address, phone, breach, breach_desc, breach_date, breach_leakcount, breach_leaktypes])

		# remove duplicates and none entries from lists
		unique_users = list(filter(None,list(dict.fromkeys(users))))
		unique_passwords = list(filter(None,list(dict.fromkeys(passwords))))
		
		for usr in unique_users:
			user_file.write(str(usr) + "\n")

		for pw in unique_passwords:
			password_file.write(str(pw) + "\n")

		user_file.close()
		password_file.close()
		
		print(bcolors.OK + "[✓]" + bcolors.ENDC + " Finished leak check on " + str(domain))
		print("    > " + str(len(unique_users)) + " unique user emails found!")
		print("    > " + str(len(unique_passwords)) + " unique passwords found!")

	except Exception as e:
		print(e)
		continue

print()
print(bcolors.INFO + "[i]" + bcolors.ENDC + " Remaining balance: " + str(balance))
