# vms

Vaccine management system

This system manages all stages of the vaccination process, from registration to recording doses.

## Environment setup instructions

**Note** These instructions assume you have `python3` and `docker` installed on your development environment.

1. `cd` into directory with `docker-compose.yml`
2. `docker-compose up` to run the containers in the foreground or `docker-compose up -d` to run them detached in the background (and `docker-compose logs -f` to tail the logs).
3. App should run on `localhost:8000`

## Stop an Environment

- If `docker-compose` is running in the foreground, `CTRL+C` should stop the containers.

- If `docker-compose` is running detached, then call `docker-compose stop` or `docker-compose down`. The difference between the two is that down will also remove the containers and networks created.

You can also run `docker-compose down -v` to delete the volumes, which contain the data and logs, when you want to start with a fresh install.

## Workflow

1. Choose or get assigned a ticket
2. Create a new branch off your team’s branch . For simplicity name your branch: `team#-issue#-brief description`.
   e.g: `git checkout -b 1-1-test team-3-vaccination`
3. Work on your code; commit & push often (so that if something comes up your team has something to work with)
4. Once done, create a pull request (PR) via git request-pull and assign it to your team lead.
5. Repeat :)

**Note** If you are behind your team's branch don't forget to run `git pull origin team-branch`
