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
parser.add_argument("--email", metavar='<email>', help="Dehashed email account", type=str, required=True)
parser.add_argument("--api-token", metavar='<token>', help="Dehashed API token", type=str, required=True)
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
dehashed_user = "<email>"
dehashed_apikey = "<api-token>"

date = datetime.now().strftime("%Y%m%d-%H%M")
balance = 0
script_dir = os.path.dirname(__file__)
try:
    os.mkdir(os.path.join(script_dir, "results/"))
except:
    pass
checkAPI = True

if (args.email):
    dehashed_user = args.email
if (args.api_token):
    dehashed_apikey = args.api_token

if (args.domains):
    with open(args.domains) as f:
        domains = f.read().split("\n")
else:
    domains = args.domain.split("\n")

domains = list(filter(None, domains))

for domain in domains:
    domain = domain.strip().strip('www.')
    url = 'https://api.dehashed.com/v2/search'
    headers = {
        "Content-Type": "application/json",
        "Dehashed-Api-Key": dehashed_apikey
    }
    json_payload = {
        "query": f"domain:{domain}",
        "size": 10000,
        "page": 1,
        "de_dupe": True,
        "wildcard": False,
        "regex": False
    }

    try:
        if checkAPI:
            print("[~] Verifying Dehashed API credentials. Please wait...")

        response = requests.post(url, headers=headers, json=json_payload)
        data = response.json()

        if response.status_code != 200:
            print(bcolors.FAIL + "[x]" + bcolors.ENDC + f" Status {response.status_code} - {data.get('error', 'Unknown error')}")
            exit()
        else:
            if checkAPI:
                print(bcolors.OK + "[✓]" + bcolors.ENDC + " Successful API authentication. Let's go looting..." + bcolors.ENDC)
                checkAPI = False
            balance = data.get('balance', 0)
            print()

        print("[~] Performing leak check on " + str(domain))

        if data.get("total", 0) == 0:
            print(bcolors.WARNING + "[✓]" + bcolors.ENDC + " Finished leak check on " + str(domain) + bcolors.ENDC)
            print("    > No leaks available.")
            continue

        if args.full:
            alldata_filename = os.path.join(script_dir, f"results/{date}_DD_{domain}_fulldata.csv")
            alldata_file = csv.writer(open(alldata_filename, "a"))
            alldata_file.writerow(["Leak ID", "Domain", "Email", "Username", "Password", "Password_Hash", "Name", "VIN", "Address", "IP Address", "Phone", "Breach", "Description", "Date", "Leak Count", "Leak Type"])

        user_file_name = os.path.join(script_dir, f"results/{date}_DD_{domain}_users.lst")
        user_file = open(user_file_name, "w")
        password_file_name = os.path.join(script_dir, f"results/{date}_DD_{domain}_passwords.lst")
        password_file = open(password_file_name, "w")

        users = []
        passwords = []

        for leak in data.get("entries", []):
            emails = leak.get("email", [])
            email = parseaddr(emails[0])[1] if emails else ""

            if f"@{domain}" not in email:
                continue

            identifier = leak.get("id", "")
            username = ",".join(leak.get("username", []))
            password = ",".join(leak.get("password", []))
            hashed_password = ",".join(leak.get("hashed_password", []))
            name = ",".join(leak.get("name", []))
            vin = ",".join(leak.get("vin", []))
            address = ",".join(leak.get("address", []))
            ip_address = ",".join(leak.get("ip_address", []))
            phone = ",".join(leak.get("phone", []))
            breach = leak.get("database_name", "")

            users.append(email)
            passwords.append(password)

            if args.full:
                breach_str = str(breach)
                breach_desc = breach_date = breach_leakcount = breach_leaktypes = ""
                if "Cit0day" in breach_str:
                    cit0day_index = next((i for i, d in enumerate(breach_data) if d["name"] == "Cit0day"), None)
                    if cit0day_index is not None:
                        breach_desc = breach_data[cit0day_index]['description']
                        breach_date = breach_data[cit0day_index]['date']
                        breach_leakcount = breach_data[cit0day_index]['leakcount']
                        breach_leaktypes = breach_data[cit0day_index]['leaktypes']
                else:
                    for leakentry in breach_data:
                        if str(leakentry.get('name', '')).lower() == breach_str.lower():
                            breach_desc = leakentry['description']
                            breach_date = leakentry['date']
                            breach_leakcount = leakentry['leakcount']
                            breach_leaktypes = leakentry['leaktypes']
                            break

                alldata_file.writerow([
                    identifier, domain, email, username, password, hashed_password, name,
                    vin, address, ip_address, phone, breach,
                    breach_desc, breach_date, breach_leakcount, breach_leaktypes
                ])

        unique_users = list(filter(None, dict.fromkeys(users)))
        unique_passwords = list(filter(None, dict.fromkeys(passwords)))

        for usr in unique_users:
            user_file.write(usr + "\n")
        for pw in unique_passwords:
            password_file.write(pw + "\n")

        user_file.close()
        password_file.close()

        print(bcolors.OK + "[✓]" + bcolors.ENDC + f" Finished leak check on {domain}")
        print(f"    > {len(unique_users)} unique user emails found!")
        print(f"    > {len(unique_passwords)} unique passwords found!")

    except Exception as e:
        print(bcolors.FAIL + f"[!] Error: {e}" + bcolors.ENDC)
        continue

print()
print(bcolors.INFO + "[i]" + bcolors.ENDC + " Remaining balance: " + str(balance))

