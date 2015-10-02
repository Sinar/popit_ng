# popit next gen

## What is this?

This is our popolo implementation, we aim to implement a few key feature

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

If you have vagrant setup, you can just use it, if you don't, bootstrap.sh and requirement.txt have the dependency you need. 

Do not use bootstap.sh in production without modification. 

After setup the dependency, you can run it on whereever you set it up with the following command

```sh
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver 0.0.0.0:8000
```

We still doing heavy development on this, consider all the step here is only for testing and development