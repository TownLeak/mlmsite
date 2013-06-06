<VirtualHost *:80>
        ServerName mlmsite.com
        ServerAlias www.mlmsite.com
        WSGIScriptAlias / /home/mlm/public_html/mlmsite.com/project.wsgi
</VirtualHost>
