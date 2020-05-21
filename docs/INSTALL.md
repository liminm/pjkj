Installation Intructions
========================

While you can run the `werkzeug`-based webserver integrated into flask during
development using `python3 -m pjkiserver`, it is not suited for production.

A full installation includes these steps:

1. Dependencies
2. Package installation
3. Web server
4. SSL setup
5. WSGI server
6. ???
7. Profit

## 1. Dependencies

Install the `mongoDB` `docker` container to provide persistent storage:
```
sudo docker pull mongo
sudo docker run --restart unless-stopped --name mongoDB -p 27017:27017 -d mongo
sudo docker start mongoDB
```
The `--restart unless-stopped` will make sure the container is started on boot
and after failures. To stop it run `sudo docker stop mongoDB`.

To reset the database, the easiest way is to re-install it:
```
sudo docker stop mongoDB
sudo docker rm mongoDB
sudo docker run --restart unless-stopped --name mongoDB -p 27017:27017 -d mongo
sudo docker start mongoDB
```

## 2. Package installation

To install the gameserver package system-wide on your system, run
```
sudo -H pip3 install --system .
```
inside of the top level repo folder. This will install the package for all
users, so your webserver user (e.g. `www-data`) can use it as well. You can
test this by leaving the folder and running `import pjkiserver` in the python3
shell from a different user.

## 3. Web server

For static files and SSL handling, a proper web server is recommended.

You can use any production web server, but we recommend `nginx`:
```
sudo apt install nginx
```
A sample site configuration file can be found in `pjki.site.nginx`. Make edits
as desired (domain name, ssl) and copy it to
`/etc/nginx/sites-available/pjki` and symlink it into `sites-enabled`:
```
sudo cp pjki.site.nginx /etc/nginx/sites-available/pjki
sudo ln -s /etc/nginx/{sites-available/pjki,/sites-enabled/pjki}
```
Then you can start `nginx` and enable it, if it isn't enabled/running yet:
```
sudo systemctl enable nginx
sudo systemctl start nginx
sudo systemctl restart nginx
```
Note that the site configuration file assumes SSL has been set up already. You
might have to disable SSL before you can get a SSL certificate.

## 4. SSL Setup

It is highly recommended to get a free SSL certificate to properly encrypt all
API (and static) traffic. This can be done easily by running `certbot`:
```
sudo -H pip3 install certbot certbot-nginx
sudo certbot
# Follow certbot's instructions
```
Instead of allowing `certbot` to change `nginx`'s configuration, it may be
easier and cleaner to just use the configuration in the given site
configuration file.

## 5. WSGI server.

WSGI is an API standard for webserver frameworks. Flask, like many other
frameworks, is WSGI compliant and thereby allows us to use a proper, high
performance HTTP middleware.

We recommend `uwsgi` because of its widespread adoption, high performance and
included `nginx` integration.

`uwsgi` should not be run manually, to ensure it operates under the same
permissions as `nginx`, only run it as `www-data`, or whatever your `nginx`
user is.
A suitable configuration file and `systemd` service file are included in this
repo, feel free to adjust them to your needs before installing:
```
sudo apt install uwsgi uwsgi-plugin-python3
sudo cp pjkiserver.service /etc/systemd/system
sudo systemctl enable pjkiserver
sudo systemctl start pjkiserver
sudo systemctl restart pjkiserver
```
This will automatically start and integrate the installed flask application
module internally by importing it.

## 6. ???

Hopefully everything worked. If not, contact [Oskar](mailto:&#119;&#105;&#110;&#107;&#101;&#108;&#115;&#64;&#99;&#97;&#109;&#112;&#117;&#115;&#46;&#116;&#117;&#45;&#98;&#101;&#114;&#108;&#105;&#110;&#46;&#100;&#101;)

You can test the API with the simplest endpoint at <https://pjki.ml/api/teams>,
`POST` a team object there and `GET` it again. The test script in `test-api.sh`
can act as a very rudimentary test when adjusting the `$HOST` variable.

## 7. Profit

You should now have a fully functional API! Now, you can add a frontend, teams,
players, get Tokens, start games and play them. Have fun!
