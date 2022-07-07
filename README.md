# CipherStock App
by XEU - V-1.3.1

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
Then, verify your requirements are all installed.
```
pip install -r pip.req
```

## Set-up
### API
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
Also, on the right conf file at /etc/mysql, change bind-address to 0.0.0.0 or to the db server ip of the interface to listen. With `py api.py sample`, you can generate sample inputs interacting with the id admin. Be sure to store an admin profile before the generation.
#### .env
You can then copy the file .env_patern into .env. Also, generate an AES key with `py api.py gen-aes`. Copy it then modify the .env as following:
 - Put the newly generated key in place of the generic one at SLE_KEY
 - Modify the upload path if needed so the uploaded files goes there, and so that the api can write there
 - You can also modify the log folder path to your accomodation
 - Finally, put all the Database informations. Be sure to let CONSTANT_DB at 0 for the first launch to allow the automatic setup of the database

Your API can be launch with `py api.py` (or `python3 api.py` or equivalent depending on the OS).

### Web app
To launch the web app, you have to simply use `py httpd.py`. The basic setup is enought for a functionnal web application
#### .env
Still, you can do some configuration in the .env :
 - CACHER_TO set the time resources are said to be kept in cache
 - HTTP_PATH set the path to the web datas
 - ERROR_TEMPLATE is the path to the html template for HTTP errors such as 404
#### Dev
To modify some vue, you'll need to modify accessible.dat and answered.dat as specified:
##### Accessible.dat
This file gives the files accessible and used in the html, such as css, js or img
##### Answered.dat
This file is a json that is used as a router. the index are the path that are answered client side, and the value of it is where the file to give is stored.

### SSL Setup
To enable the SSL socket, you'll need the key file and certification file on your server. You'll simply need to go modify your .env as following:
 - Set SSL_ON as 1
 - Set the two path so the api can find your key and certification
 - ensure the api has the permisions to read those files

### Recommended structure
We reccomand a structure of 4 servers on Debian. Be careful to make a password policy and to make right priviledges for the users and administrators.

#### The Firewall
##### /etc/networking/interfaces
 - external interfaces, most likely NAT or private host network interface
 - internal interface with static ip (suggested 172.16.42.9/30)
##### /etc/sysctl.conf
Don't forget to uncomment ip_forwarding
##### NAT configuration
Many things can be done, and you're quite free depending on your external interfaces. Tho we recemand the following :
 - SNAT allowing internal ips to ping internet (suggested 172.16.42.8/30)
 - REDIRECT 80 to 443
 - DNAT the port 3443 to your api server on the corresponding ports (suggested 172.16.42.10:3333-3443)
 - DNAT the port 443 to your web server on the corresponding ports (suggested 172.16.42.11:400-443)

#### The Database
##### Interface
 - Internal network, static ip (recommended 172.16.42.12/30)
 - Gateway 172.16.42.9
##### Setup
Cf [API](#api)
With our recommended ip, it gives
```
apt install default-mysql-server
mysql
```
```SQL
CREATE DATABASE xeu;
CREATE USER api@172.16.42.10 identified by "iamanagreaggatedapi";
GRANT SELECT, DELETE, INSERT, ALTER, CREATE on xeu.* to api@172.16.42.10;
FLUSH PRIVILEGES;
```
##### Whitelist
On /etc/mysql, find the conf file with bind-adress and set it to the adress of your api (recommended 172.16.42.10) for making only this adress able to connect to the db. 

#### The API server
##### Interface
 - Internal network, static ip (recommended 172.16.42.10/30)
 - Gateway 172.16.42.9
##### Setup
Clone the git on the server (recommended on /etc/cypherstock/), and follow the [installation instructions](#api). Don't forget to activate [SSL](#ssl-setup) You can add a bash script to facilitate the launching such as:
```
cd /etc/cypherstock/
py src/api.py
```
##### In the future
On futur versions, you will be able to put multiple daoemons. This will allow to launch on multiple ports, and so it will allow to manage more requests

#### The Web server
##### Interface
 - Internal network, static ip (recommended 172.16.42.11/30)
 - Gateway 172.16.42.9
##### Setup
Clone the git on the server (recommended on /etc/cypherstock/), and follow the [installation instructions](#web-app). Don't forget to activate [SSL](#ssl-setup) You can add a bash script to facilitate the launching such as:
```
cd /etc/cypherstock/
py src/api.py
```
##### In the future
On futur versions, you will be able to put multiple daoemons. This will allow to launch on multiple ports, and so it will allow to manage more requests



## Security notice
- This work has not been submitted to any audit, and does not have any pretention to say being fully secured.
- The web app is the most likely vulnerable since it has been the less reviewed.
- A full setup test has not been done, which means pip.req can be incomplete right now.
- The CLI are not properlly finished. They may be used for malicious reasons we don't know.
- Error Management is not operationnal in this current version. It will not give all informations when stopping a request.
- Anti-DDoS has a place to come for future versions, but is not implemented


## Architecture
 - .env_patern : a model for the dotenv to use as a setting file
 - pip.req : a pip requirement file for the project
 - README.md
 - .gitignore & .gitattributes
### RCS Folder
 - archi.json : json for the automatic setup of the database
#### Log Folder
 - db.log : log of all input to database
 - verif-string : log of all irregular input string
#### SSL Folder
Folder to fill in the setup with SSL key and certificate
#### Upload Folder
Folder where the uploaded files are saved
### SRC Folder
 - api.py : CLI for the API part of the project. Do api.py h to get more informations
 - cypherstock.py : CLI for basic client-side functions
 - httpd.py : CLI for web app
#### Serve Folder
 - db.py : lib related to mysql. Create an instance to use for fetching and commiting. Verify every requests with FA or auth token
 - exeptions.py : lib of all custom exeptions (incomplete)
 - FA.py : lib for working 2FA
 - lib.py : lib for the sockets of the API and the web app
#### Front Folder
 - accessible.dat & answered.dat : router setting files
 - app.html : html for the web app
 - index.html : html for the unlogged people (login & signup)
 - error.html : template for the HTTP errors
##### CSS
 - norm.css : css normalisation between browsers
 - index.css : css for index.html
 - app.css : css for app.html
 - dark.css : dark theme
 - light.css : light theme
##### JS
 - script.js : common js
 - index.js : js for index.html
 - app.js : js for app.html
##### RCS
folder for non-text resources, like png

