# vms

Vaccine management system

This system manages all stages of the vaccination process, from registration to recording doses.

## Environment setup instructions

To set up the database connection:

1. copy `local.template.cnf` and rename it to `local.cnf`
2. add your logging credentials where needed

It is _VERY_ important to only add credentials in `local.cnf`. Add it anywhere else and you are compromising people's privacy.

## Start an Environment

**Note** These instructions assume you have `python3` and `docker` installed on your development environment.

1. `cd` into directory with `docker-compose.yml`
2. `docker-compose up` to run the containers in the foreground or `docker-compose up -d` to run them detached in the background (and `docker-compose logs -f` to tail the logs).
3. App should run on `localhost:8000`

**Note** If you are making changes to the environement docker-compose will not rebuild automatically, so run `docker-compose up --build`

## Stop an Environment

- If `docker-compose` is running in the foreground, `CTRL+C` should stop the containers.

- If `docker-compose` is running detached, then call `docker-compose stop` or `docker-compose down`. The difference between the two is that down will also remove the containers and networks created.

You can also run `docker-compose down -v` to delete the volumes, which contain the data and logs, when you want to start with a fresh install.

## Workflow

0. Run `pre-commit install` - you'll only need to do this once and your code will be automatically tidied after you attempt to `git commit`.
1. Choose or get assigned a ticket
2. Create a new branch off your team’s branch . For simplicity name your branch: `team#-issue#-brief description`.
   e.g: `git checkout -b 3-1-test team-3-vaccination`
3. Work on your code; commit often (so that if something comes up your team has something to work with)
4. Once done, create a pull request (PR) via git request-pull and assign it to your team lead.
5. Repeat :)

Instructions for setting up MySQL locally (if not using Docker):

NOTE: MacOS instructions below. If you have a Windows machine, add to this README once you've figured it out :)

1. Install homebrew (google it!)
2. `brew install mysql`
3. `mysql.server start`
4. Find the path to your mysql installation with `brew info mysql`.
5. You can play around with the REPL with `path/to/mysql -u root`.
6. In the REPL, create a local mysql database called `vms`:
   - Run `path/to/mysql -u root` to open the REPL
   - Run `CREATE DATABASE vms;` to create the `vms` database
     If the command was successful, running `SHOW DATABASES` should list `vms` as one of the databases.
7. Sequel Pro is a nice (free) GUI client for interacting with your DB, to set it up to connect with your mysqlserver, you might have to open the REPL and run the following: `ALTER USER root@localhost IDENTIFIED WITH mysql_native_password BY '';`

   - `local.cnf` is a configuration file that django uses to access your local database. If you want to use your own config feel free to modify your local version of the file with your own credentials.

8. Success! Ping wuharvey@gmail.com with Q's.
