# popit next gen

## What is this?

This is our popolo implementation, we aim to implement a few key features

1. Person, Org, Post, Membership entity based on popolo. Other entity will come later. 
2. Have good multilingual support as Malaysia uses multiple languages
3. Implementing extra feature without breaking support for popolo
4. Strong citation
5. API with support for json
6. Basic admin page for data entry. 

## How to run this?

This project uses:

* python
* django
* postgresql

If you have vagrant setup, you can just use it, if you don't, `bootstrap.sh` and `requirement.txt` have the dependencies you need. 

Please do not use `bootstap.sh` in production without modification. 

After setting up the dependencies, you can run it on whereever you want with the following command

```sh
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver 0.0.0.0:8000
```

We still doing heavy development on this, so all the steps here are for testing and development.

## Current feature
1. CRUD API for Person, Organization, Post, Membership following popolo standarrd
2. Implement Othername, ContactDetails, Area, Links, Identifier following popolo standard
3. Search API for Person, Organization, Post, Membership. Including any entity on 2. that is embedded. 
4. Multilingual support for the feature 1., 2. and 3.
5. Support for json output
6. Support for API to be displayed on browser
7. Extensive supporting unit test for supported feature
8. extend links to support citation by having an optional field value, no API to easily browse citation yet
