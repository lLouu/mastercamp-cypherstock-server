# CipherStock App
by XEU

## Main informations
This project has been made in an academical context in EFREI PARIS, for preparing Masters in CyberSecurity and Network. It has been done in Python, however the idea is to get the most low-level we can to fully understand and have control over what's happening on the trafics. This app has been thought to be run on three server : the API ; the DB ; and the web app. The main functions reside in the API. However, many cryptology concepts are needed to understand the client side of the web app.

## Installation
### Linux Debian
Firstly, ensure you have some of the main package
```
apt update
apt install python3 python3-pip git
```

Clone the repo using git
```
git clone https://github.com/lLouu/mastercamp-cypherstock-server [path-to-download]
```

## Set-up
### API
First, verify your requirements are all installed.
```
pip install -r pip.req
```
#### Database
You will also need a mysql database somewhere you can connect to. You only need to create a database and a user for the api. This user should be able at leaste to SELECT, DELETE, INSERT and, for the automatic database set-up, ALTER and CREATE. On linux, you can do the following
```
apt install default-mysql-server
mysql
```
```SQL
CREATE DATABASE xeu;
CREATE USER api@<api-server-ip> identified by "iamanagreaggatedapi";
GRANT SELECT, DELETE, INSERT, ALTER, CREATE on xeu.* to api@<api-server-ip>;
FLUSH PRIVILEGES;
```
Also, on the right conf file at /etc/mysql, change bind-address to 0.0.0.0 or to the db server ip of the interface to listen
#### .env
You can then copy the file .env_patern into .env. Also, generate an AES key with `py api.py gen-aes`. Copy it then modify the .env as following:
 - Put the newly generated key in place of the generic one at SLE_KEY
 - Modify the upload path if needed so the uploaded files goes there, and so that the api can write there
 - You can also modify the log folder path to your accomodation
 - Finally, put all the Database informations. Be sure to let CONSTANT_DB at 0 for the first launch to allow the automatic setup of the database

Your API can be launch with `py api.py` (or `python3 api.py` or equivalent depending on the OS).

### SSL Setup
To enable the SSL socket, you'll need the key file and certification file on your server. You'll simply need to go modify your .env as following:
 - Set SSL_ON as 1
 - Set the two path so the api can find your key and certification
 - ensure the api has the permisions to read those files


