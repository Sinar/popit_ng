#!/usr/bin/env bash
apt-get update
apt-get install -y redis-server python-setuptools python-dev postgresql postgresql-server-dev-all python-pip \
    build-essential postgresql-contrib
pip install -r /vagrant/requirement.txt
sudo -u postgres psql -c "create database popit"
sudo -u postgres psql -c "create user popit with password 'password'" # Change this in production
sudo -u postgres psql -c "grant all privileges on database popit to popit"
# DO NOT USE THE LINE BELOW IN PRODUCTION. THIS IS FOR VAGRANT ONLY
sudo -u postgres psql -c "ALTER USER popit WITH CREATEDB;"
apt-get install -y openjdk-7-jre unzip
wget https://download.elasticsearch.org/elasticsearch/release/org/elasticsearch/distribution/zip/elasticsearch/2.1.0/elasticsearch-2.1.0.zip
unzip elasticsearch-2.1.0.zip
