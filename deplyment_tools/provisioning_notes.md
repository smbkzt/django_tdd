First add a sudo user
========================

useradd -m -s /bin/bash smbkzt
usermod -a -G sudo smbkzt
passwd smbkzt
su - smbkzt


Install packages
====================
sudo apt-get update
sudo apt-get install python3-pip python3-dev libpq-dev nginx

sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv


Create a folder to project
==========================
mkdir bla bla bla


Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3.6
* virtualenv + pip
* Git

eg, on Ubuntu:

    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get update
    sudo apt-get install nginx git python36 python3.6-venv

## Nginx Virtual Host config

* see nginx.template.conf
* replace SITENAME with, e.g., staging.my-domain.com

## Systemd service

* see gunicorn-systemd.template.service
* replace SITENAME with, e.g., staging.my-domain.com

## Folder structure:
Assume we have a user account at /home/username

/home/username
└── sites
    └── SITENAME
         ├── database
         ├── source
         ├── static
         └── virtualenv
