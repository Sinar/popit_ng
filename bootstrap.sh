#!/usr/bin/env bash
apt-get update
apt-get install -y redis-server python-setuptools python-dev postgresql postgresql-server-dev-all python-pip \
    build-essential postgresql-contrib
pip install -r requirement.txt
sudo -u postgres psql -c "create database popit"
sudo -u postgres psql -c "create user popit with password 'password'" # Change this in production
sudo -u postgres psql -c "grant all privileges on database popit to popit"