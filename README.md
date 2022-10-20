# DehashedDumper
Python3 script to dump breach data from Dehashed.

Either takes a single domain name or a file with newline separated domain names. Queries breach data for each domain on dehashed.com and outputs unique usernames and leaks into outfiles. If you supply the `--full` command, all breach data from Dehashed's API are stored in an additional outfile.

## Usage
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

## Example Output
````
$ python3 dehasheddumper.py --domains domains.txt

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
.rw-r--r-- anon anon 148 B  Thu Oct 20 18:13:04 2022   20102022_DD_apple.com_passwords.lst 
.rw-r--r-- anon anon 122 B  Thu Oct 20 18:13:04 2022   20102022_DD_apple.com_users.lst     
.rw-r--r-- anon anon 4.7 KB Thu Oct 20 18:13:44 2022   dehasheddumper.py
````
