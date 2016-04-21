#!/usr/bin/env bash
apt-get update
apt-get install -y redis-server python-setuptools python-dev postgresql postgresql-server-dev-all python-pip \
    build-essential postgresql-contrib
pip install -r /vagrant/requirements.txt
sudo -u postgres psql -c "create database popit"
sudo -u postgres psql -c "create user popit with password 'password'" # Change this in production
sudo -u postgres psql -c "grant all privileges on database popit to popit"
# DO NOT USE THE LINE BELOW IN PRODUCTION. THIS IS FOR VAGRANT ONLY
sudo -u postgres psql -c "ALTER USER popit WITH CREATEDB;"
apt-get install -y openjdk-7-jre unzip
wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
echo "deb http://packages.elastic.co/elasticsearch/2.x/debian stable main" | sudo tee -a /etc/apt/sources.list.d/elasticsearch-2.x.list
sudo apt-get update && sudo apt-get install elasticsearch

# Ensure when login via shell it goes to the code
echo -e "\ncd /vagrant" >>~/.bashrc
