Deployment Intructions
======================

While you can run the `werkzeug`-based webserver integrated into flask during
development using `python3 -m pjkiserver`, it is not suited for production.

If you just want to install the test server on your system, but not run a full
production enviroment, DO NOT FOLLOW THESE INSTRUCTIONS. These are for
permanent deployments only.

Commands are used and tested on Debian 10.

A full deployment includes these steps:

1. Dependencies
2. Package installation
3. Web server
4. SSL setup
5. WSGI server
6. ???
7. Profit

## 1. Dependencies

Install the dependencies:

For mongoDB, first add their apt sources as described on
[their website](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-debian/).

Do a full update + upgrade:
```
sudo apt update
sudo apt upgrade
```

Then, install all required backages
```
# Debian
sudo apt install \
	git python3 python3-pip \
	nginx certbot python3-certbot-nginx \
	uwsgi uwsgi-plugin-python3 \
	mongodb-org
```

Unfortunately, the service file shipped by mongo has an error in it. Let's fix
that. Edit the file:
```
sudo nano /lib/systemd/system/mongod.service
```
and replace the line
```
PIDFile=/var/run/mongodb/mongod.pid
```
with
```
PIDFile=/run/mongodb/mongod.pid
```

Then, start mongoDB using
```
sudo systemctl daemon-reload
sudo systemctl enable mongod
sudo systemctl restart mongod
```
and ensure there are no errors.

## 2. Package installation

Download the gameserver source onto your drive:
```
git clone https://gitlab.tubit.tu-berlin.de/PJ-KI/server.git pjkiserver
```

To install the gameserver package system-wide on your system, run
```
cd pjkiserver
sudo -H pip3 install --system -r requirements.txt
sudo -H pip3 install --system .
```
This will install the package for all users, so your webserver user (e.g.
`www-data`) can use it as well. You can test this by *leaving the folder* and
running `import pjkiserver` in the python3 shell from a different user.

## 3. Web server

For static files and SSL handling, a proper web server is recommended. You can
use any production web server, but we recommend `nginx`.

A sample site configuration file can be found in `pjki.site.nginx`. Make edits
as desired (domain name, ssl) and copy or symlink it to
`/etc/nginx/sites-available/pjki`, then symlink it into `sites-enabled`:
```
sudo cp pjki.site.nginx /etc/nginx/sites-available/pjki
sudo ln -s /etc/nginx/{sites-available/pjki,/sites-enabled/pjki}
```
Then you can start `nginx` and enable it, if it isn't enabled/running yet:
```
sudo systemctl enable nginx
sudo systemctl restart nginx
```
Note that the site configuration file assumes SSL has been set up already. You
might have to disable SSL before you can get a SSL certificate.

## 4. SSL Setup

It is highly recommended to get a free SSL certificate to properly encrypt all
API (and static) traffic. This can be done easily by running `certbot`:
```
sudo certbot
# Follow certbot's instructions
```
When `certbot` asks you if you want it to add redirects, decline because the
provided config file already does that.

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
repo.

IMPORTANT: Edit the `pjkiserver.service` file to update the `uswsgi.ini` file
path inside.

Then, copy or symlink the service file into `systemd`:
```
sudo cp pjkiserver.service /etc/systemd/system
sudo systemctl daemon-reload
```
One more thing: To avoid a permission error, initialize `uwsgi`'s logfile to be
owned by your webserver user:
```
sudo touch /var/log/uwsgi.log
sudo chown www-data:www-data /var/log/uwsgi.log
```
Finally, let's start the server.
```
sudo systemctl enable pjkiserver
sudo systemctl restart pjkiserver
```
This will automatically start and integrate the installed flask application
module internally by importing it.

## 6. ???

You can check if everything is running by checking the status of `nginx`,
`mongod` and `pjkiserver` by visiting their `systemd` status page:
```
sudo systemctl status <service (nginx, mongod, pjkiserver) >
```
More debugging info can be found in `sudo journalctl -xe` as well as `nginx`'
and `uwsgi`'s log files (`/var/log/nginx/{access,error}.log`,
`/var/log/uwsgi.log`).

You can test the API with the simplest endpoint at <https://pjki.ml/api/teams>,
`POST` a team object there and `GET` it again. The test script in `test-api.sh`
can act as a very rudimentary test when adjusting the `$HOST` variable.

Hopefully everything worked. If not, contact
[Oskar](mailto:&#119;&#105;&#110;&#107;&#101;&#108;&#115;&#64;&#99;&#97;&#109;&#112;&#117;&#115;&#46;&#116;&#117;&#45;&#98;&#101;&#114;&#108;&#105;&#110;&#46;&#100;&#101;)

## 7. Profit

You should now have a fully functional API! Now, you can add a frontend, teams,
players, get Tokens, start games and play them. Have fun!
