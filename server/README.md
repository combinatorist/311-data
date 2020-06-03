

### Getting started

1. Install docker, docker-compose and git

2. clone this repo and `cd` into the `server` directory

3. run the install script

4. check your setup

5. populate your database

  1. get a socrata token from someone on the team, and add it to you .env file

  2. choose the years you want to add, and set INGEST_YEARS in your .env file

  3. run this command: `docker-compose run server python bin/db_ingest.py`


### Development
```
docker-compose up --build
```

#### Linting
```
docker-compose run server flake8 ..
```

#### Running tests (disabled until we get a test DB up)
```
docker-compose run server pytest ..
```

#### Database updates
```
docker-compose run server python bin/db_update.py
```
