<VirtualHost *:80>
        ServerName mlmsite.com
        ServerAlias www.mlmsite.com
        WSGIScriptAlias / /home/mlm/public_html/mlmsite.com/project.wsgi
        Alias /static/ /home/mlm/public_html/mlmsite.com/
        <Location "/static/">
            Options -Indexes
        </Location>
</VirtualHost>
