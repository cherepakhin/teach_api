WSGIPythonHome "/home/vasi/rshop/env"

<VirtualHost *:80>
	ServerName m.el59.ru

	DocumentRoot /var/www/m
	<Directory />
		Options FollowSymLinks
		AllowOverride All
		allow from all
	</Directory>

	WSGIProcessGroup rshop
	WSGIDaemonProcess rshop user=vasi group=vasi threads=5
	WSGIScriptAlias /rshop /home/vasi/rshop/django.wsgi

#	<Directory /rshop>
#    	    WSGIProcessGroup rshop
#            WSGIApplicationGroup %{GLOBAL}
#    	    Order deny,allow
#            Allow from all
#	</Directory>
	
	Alias /favicon.ico /var/www/m/public/favicon.ico

#	Alias / /var/www/m/index.html
#	Alias /index.html /var/www/m/index.html

	Alias /public/ /var/www/m/public/
	
	<Location /public/>
    	    Options -Indexes
        </Location>

	Alias /static/ /var/www/m/static/
	
	<Location /static/>
    	    Options -Indexes
        </Location>

	ErrorLog ${APACHE_LOG_DIR}/m.el59.ru/error.log
	LogLevel warn
	CustomLog ${APACHE_LOG_DIR}/m.el59.ru/access.log combined
</VirtualHost>
