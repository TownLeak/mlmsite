#! /bin/bash

ROOT=/home/mlm/public_html/mlmsite.com

cd $ROOT
git pull
pushd DiamondMLM
ln -sf settings_prod.py settings_actual.py
popd
rm database
python manage.py syncdb --noinput
python manage.py collectstatic --noinput
chmod 666 database
sudo /etc/init.d/apache2 reload
