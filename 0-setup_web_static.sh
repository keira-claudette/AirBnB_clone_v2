#!/usr/bin/env bash
# sets up your web servers for the deployment of web_static
# Read: https://www.geeksforgeeks.org/mkdir-command-in-linux-with-examples/
sudo apt-get -y update
sudp apt-get -y install nginx
ufw allow 'Nginx HTTP'
mkdir -p /data/web_static/
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/
echo "<html>
  <head>
  </head>
  <body>
    <p>Testing Nginx configuration</p>
    <p>Holberton School</p>
  </body>
</html>" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test /data/web_static/current
chown -R ubuntu:ubuntu /data
sed -i '/listen 80 default_server/a location /hbnb_static/ { alias /data/web_static/current/;}' /etc/nginx/sites-available/default
exit 0
