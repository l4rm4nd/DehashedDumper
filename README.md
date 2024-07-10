<div align="center" width="100%">
    <h1>DehashedDumper</h1>
    <p>Python3 script to dump breach data from Dehashed</p><p>
    <a target="_blank" href="https://github.com/l4rm4nd"><img src="https://img.shields.io/badge/maintainer-LRVT-orange" /></a>
    <a target="_blank" href="https://GitHub.com/l4rm4nd/DehashedDumper/graphs/contributors/"><img src="https://img.shields.io/github/contributors/l4rm4nd/DehashedDumper.svg" /></a><br>
    <a target="_blank" href="https://GitHub.com/l4rm4nd/DehashedDumper/commits/"><img src="https://img.shields.io/github/last-commit/l4rm4nd/DehashedDumper.svg" /></a>
    <a target="_blank" href="https://GitHub.com/l4rm4nd/DehashedDumper/issues/"><img src="https://img.shields.io/github/issues/l4rm4nd/DehashedDumper.svg" /></a>
    <a target="_blank" href="https://github.com/l4rm4nd/DehashedDumper/issues?q=is%3Aissue+is%3Aclosed"><img src="https://img.shields.io/github/issues-closed/l4rm4nd/DehashedDumper.svg" /></a><br>
        <a target="_blank" href="https://github.com/l4rm4nd/DehashedDumper/stargazers"><img src="https://img.shields.io/github/stars/l4rm4nd/DehashedDumper.svg?style=social&label=Star" /></a>
    <a target="_blank" href="https://github.com/l4rm4nd/DehashedDumper/network/members"><img src="https://img.shields.io/github/forks/l4rm4nd/DehashedDumper.svg?style=social&label=Fork" /></a>
    <a target="_blank" href="https://github.com/l4rm4nd/DehashedDumper/watchers"><img src="https://img.shields.io/github/watchers/l4rm4nd/DehashedDumper.svg?style=social&label=Watch" /></a><br>
    <a target="_blank" href="https://hub.docker.com/r/l4rm4nd/dehasheddumper"><img src="https://badgen.net/badge/icon/l4rm4nd%2Fdehasheddumper:latest?icon=docker&label" /></a><br><p>
    <a href="https://www.buymeacoffee.com/LRVT" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>
</div>

## 💬 Description

DehashedDumper is a Python 3 script that dumps breach data from the [Dehashed Leak API](https://dehashed.com).

The script either takes a single domain name or a file with newline separated domain names. It will then query breach data for each target domain and output the results into outfiles. If you supply the `--full` command, all breach data from Dehashed's API is stored in a separate CSV outfile. The CSV will be extended with private information about breaches, e.g. a description, the breach date as well as the amount and type of leaked data.

## ✨ Requirements

DehashedDumper talks with the official Dehashed API, which requires authentication. Therefore, you must have a valid subscription and enough API tokens on Dehashed. You can retrieve your API key from your [Dehashed profile](https://dehashed.com/profile). Use your email address for the API authentication.

Your authentication credentials are passed via the CLI parameters `--email` and `--api-token`. 

## 🎓 Usage

````
usage: dehasheddumper.py [-h] (--domain <domain> | --domains <file>) [--email <email>] [--api-token <token>] [--full]

options:
  -h, --help              show this help message and exit
  --domain <domain>       Domain name to extract leaks
  --domains <file>        Newline separated file with domain names
  --email <email>         Dehashed email account
  --api-token <token>     Dehashed API token
  --full                  Dump all data from Dehashed into CSV
````


### 🐳 Example 1 - Docker Run

````
docker run --rm -v ${PWD}:/app/results l4rm4nd/dehasheddumper:latest --domain apple.com --email <email> --api-token <token> --full
````

### 🐍 Example 2 - Native Python

````
# install dependencies
pip install -r requirements.txt

python3 dehasheddumper.py --domain apple.com --email <email> --api-token <token> --full
````

## 💎 Outputs

````
$ python3 dehasheddumper.py --domains domains.txt --full

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

[i] Performing leak check on apple.com
[i] Finished leak check on apple.com
    > 42 unique user emails found!
    > 1000 unique passwords found!
    
    
$ ls -la  
.rw-r--r-- anon anon 148 B  Thu Oct 20 18:13:04 2022   20102022-1337_DD_apple.com_passwords.lst 
.rw-r--r-- anon anon 122 B  Thu Oct 20 18:13:04 2022   20102022-1337_DD_apple.com_users.lst    
.rw-r--r-- anon anon 08 KB  Thu Oct 20 18:13:04 2022   20102022-1337_DD_apple.com_fulldata.lst
.rw-r--r-- anon anon 04 KB  Thu Oct 20 18:13:44 2022   dehasheddumper.py
````
