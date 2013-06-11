#! /bin/bash

ROOT=/home/mlm/public_html/mlmsite.com

cd $ROOT
git pull
pushd DiamondMLM
ln -sf settings_prod.py settings_actual.py
sudo /etc/init.d/apache2 reload
popd
