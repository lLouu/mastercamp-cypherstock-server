# CipherStock App
by XEU

## Main informations
This project has been made in an academical context in EFREI PARIS, for preparing Masters in CyberSecurity and Network. It has been done in Python, however the idea is to get the most low-level we can to fully understand and have control over what's happening on the trafics. This app has been thought to be run on three server : the API ; the DB ; and the web app. The main functions reside in the API. However, many cryptology concepts are needed to understand the client side of the web app.

## Installation
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
You will also need a mysql database somewhere you can connect to. You only need to create a database and a user for the api. This user should be able at leaste to SELECT, DELETE, INSERT and, for the automatic database set-up, ALTER TABLE and CREATE TABLE. You can then copy the file .env_patern into .env. Also, generate an AES key with `py api.py gen-aes`. Copy it then modify the .env as following:
 - Put the newly generated key in place of the generic one at SLE_KEY
 - Modify the upload path if needed so the uploaded files goes there, and so that the api can write there
 - You can also modify the log folder path to your accomadation
 - Finally, put all the Database informations. Be sure to let CONSTANT_DB at 0 for the first launch to allow the automatic setup of the database

Your API can be launch with `py api.py`.

### SSL Setup
To enable the SSL socket, you'll need the key file and certification file on your server. You'll simply need to go modify your .env as following:
 - Set SSL_ON as 1
 - Set the two path so the api can find your key and certification
 - ensure the api has the permisions to read those files

### Client-side basics


