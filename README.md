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
