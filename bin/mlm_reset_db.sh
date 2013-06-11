#! /bin/bash

rm database
python manage.py syncdb --noinput
python manage.py runserver
