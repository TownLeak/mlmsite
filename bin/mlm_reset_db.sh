#! /bin/bash

rm database
python manage.py syncdb
pyhton manage.py runserver
