# popit next gen

## What is this?

This is our popolo implementation, we aim to implement a few key features

1. Person, Org, Post, Membership entities based on popolo. Other entities will come later. 
2. Have good multilingual support as Malaysia uses multiple languages.
3. Implementing extra features without breaking support for popolo.
4. Strong citations.
5. API with support for json.
6. Basic admin page for data entry. 

## How to run this?

This project depends on:

* python
* django
* postgresql
* elasticsearch

If you have vagrant setup, you can just use it, if you don't, `bootstrap.sh` and `requirement.txt` have the dependencies you need. 

Please do not use `bootstap.sh` in production without modification. 

After setting up the dependencies, you can run it with the following command, assuming that you are on vagrant:

```sh
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver 0.0.0.0:8000
$ cd /home/vagrant/elasticsearch*
$ bin/elasticsearch
```

Now indexing is a separate service using celery, run it with the following command

```sh
$ celery worker -A popit_ng -l info
```

Currently index in elasticsearch is not cleaned after an entity is deleted. Run the following to clean it. 
 In production this should be a cronjob

```sh
python manage.py clean_index
```

If you're not on vagrant, change to the directory you install elasticsearch on. I assume that you are doing a manual installation
for development.

To create new test data

```sh
$ python manage.py dumpdata popit auth authtoken contenttypes --output popit/fixtures/api_request_test_data.yaml --format yaml --natural-foreign --natural-primary
```

To load test data

```sh
$ python manage.py loaddata popit/fixtures/api_request_test_data.yaml
```

* username is admin, password is rockgod. Don't use it for production
* auth token is 04afcac1d644e3dbab187d8b2205d355c0d9b951.
* token is set http header "Authorization: Token 04afcac1d644e3dbab187d8b2205d355c0d9b951"
* test data is not loaded into elasticsearch. But there is a reindex command to add data to elasticsearch

```sh
$ python manage.py reindex
```

We are still doing heavy development on this project, so all the steps here are for testing and development only.

## Current features
1. CRUD API for Person, Organization, Post, Membership following popolo standard.
2. Implement Othername, ContactDetails, Area, Links, Identifier following popolo standard.
3. Search API for Person, Organization, Post, Membership. Including any entity on 2. that is embedded. 
4. Multilingual support for the feature 1., 2. and 3.
5. Support for json output.
6. Support for API to be displayed on browser.
7. Extensive supporting unit test for supported feature.
8. Extend links to support citation by having an optional field value. There no API to easily browse citations yet.
