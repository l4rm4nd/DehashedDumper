import requests
import json
import argparse
from datetime import datetime

parser = argparse.ArgumentParser("dehasheddumper.py")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--domain", metavar='<domain>', help="Domain name to extract leaks", type=str, required=False)
group.add_argument("--domains", metavar='<file>', help="Newline separated file with domain names", required=False)
parser.add_argument("--email", metavar='<email>', help="Dehashed email account", type=str, required=False)
parser.add_argument("--api-token", metavar='<token>', help="Dehashed API token", type=str, required=False)
parser.add_argument("--full", help="Dump all data from Dehashed into CSV", required=False, action='store_true')

args = parser.parse_args()

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

date = datetime.now().strftime("%d%m%Y")

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

	print("[i] Performing leak check on " + str(domain))

	try:
		response = requests.get(url, params=params, headers=headers, auth=(dehashed_user, dehashed_apikey))
		# file containing user email addresses
		user_file = open(str(date) + "_DD_" + str(domain) + "_users.lst", "a")
		# file containing leaked user passwords
		password_file = open(str(date) + "_DD_" + str(domain) + "_passwords.lst", "a")
		# convert response to json
		data = response.json()
		# list to store user emails
		users = []
		# list to store user passwords
		passwords = [] 

		for leak in data['entries']:
			identifier=str(leak['id'])
			email=str(leak['email'])
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
				alldata_file = open(str(date) + "_DD_" + str(domain) + "_fulldata.csv", "a")
				alldata_file.write(identifier+","+email+","+username+","+password+","+hashed_password+","+name+","+vin+","+address+","+ip_address+","+phone+","+breach+"\n")
				alldata_file.close()

		# remove duplicates from lists
		unique_users = list(dict.fromkeys(users))
		unique_passwords = list(dict.fromkeys(passwords))

		for usr in unique_users:
			user_file.write(str(usr) + "\n")

		for pw in unique_passwords:
			password_file.write(str(pw) + "\n")

		user_file.close()
		password_file.close()
		print("[i] Finished leak check on " + str(domain))
		print("    > " + str(len(unique_users)) + " user mail found!")
		print("    > " + str(len(unique_passwords)) + " passwords found!")
		print()

	except Exception as e:
		print(e)
		continue
