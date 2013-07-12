#! /bin/bash

rm database
python manage.py syncdb --noinput
python manage.py migrate
python manage.py runserver -v 3 0.0.0.0:8000
