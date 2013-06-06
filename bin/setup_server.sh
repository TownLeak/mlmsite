#! /bin/bash

USER=mlm
SSH_CONFIG_FILE=/etc/ssh/sshd_config
APT_COMMAND="sudo aptitude install -y"
EASY_INSTALL="sudo easy_install"
APPLICATION_NAME=mlmsite
SITE_NAME=${APPLICATION_NAME}.com
HTML_ROOT=$HOME/public_html/
SITE_ROOT=$HTML_ROOT/$SITE_NAME

adduser $USER
visudo
echo "UseDNS no" >> $SSH_CONFIG_FILE
echo "AllowUsers $USER" >> $SSH_CONFIG_FILE
echo "PermitRootLogin no" >> $SSH_CONFIG_FILE
$APT_COMMAND python-imaging python-pythonmagick python-markdown python-textile python-docutils python-django
$APT_COMMAND libapache2-mod-wsgi apache2 apache2.2-common apache2-mpm-prefork apache2-utils libexpat1 ssl-cert
$APT_COMMAND git vim
$APT_COMMAND python-setuptools
reload ssh
ssh-keygen
nano .ssh/authorized_keys
sudo service apache2 restart
mkdir -p $HTML_ROOT
cd $HTML_ROOT
git clone https://github.com/rossz/mlmsite.git $SITE_NAME
sudo locale-gen hu_HU
sudo update-locale LANG=hu_HU
cp $SITE_ROOT/config/bashrc $HOME/.bashrc
source $HOME/.bashrc
sudo cp $SITE_ROOT/config/apache_site_conf_$SITE_NAME /etc/apache2/sites-available/$SITE_NAME
sudo a2dissite default
sudo a2ensite $SITE_NAME
sudo /etc/init.d/apache2 reload
$EASY_INSTALL South
$EASY_INSTALL django-countries
$EASY_INSTALL django-userena
$EASY_INSTALL django-bootstrap-toolkit
sudo apt-get build-dep python-imaging
chmod 777 $SITE_ROOT # http://bit.ly/13e3jU4

