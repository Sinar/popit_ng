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

If you have vagrant setup, you can just use it, if you don't, `bootstrap.sh` and `requirement.txt` have the dependencies you need. 

Please do not use `bootstap.sh` in production without modification. 

After setting up the dependencies, you can run it with the following command:

```sh
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver 0.0.0.0:8000
```

To load test data

```sh
$ python manage.py loaddata popit/fixtures/api_request_test_data.yaml
```

* username is admin, password is rockgod. Don't use it for production
* auth token is 04afcac1d644e3dbab187d8b2205d355c0d9b951.
* token is set http header "Authorization: Token 04afcac1d644e3dbab187d8b2205d355c0d9b951"

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
