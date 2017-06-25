Provisioning a new site
========================

* nginx
* python 3.4
* Git
* pip
* virtualenv

eg on ubuntu:
	sudo apt-get install nginx git python3 python3-pip
	sudo pip3 install virtualenv
	
## nginx virtual host config

* see nginx.template.conf
* replace SITENAME with, eg., staging.my-domain.com	

## Upstart job

* see gunicorn-upstart.template.conf
* replace SITENAME with, eg., staging.my-domain.com

## folder Structure:
Assuming we have a user account at /home/username

/home/username
*   sites/
*        SITENAME/
*			database/
*			source/
*			static/
*	virtualenv/
			
