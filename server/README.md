

## Setup

1. Install docker, docker-compose and git

2. clone this repo and `cd` into the `server` directory

3. create .env file and add socrata token

from this directory run `cp .env.example .env`
then get a socrata token from someone on the team and add it to the .env file

3. build your containers: `docker-compose build`

4. Seed your local DB: `docker-compose run server python bin/ingest.py`


## Development
```
docker-compose up --build
```

## Linting
```
docker-compose run server flake8 ..
```

## Running tests (disabled until we get a test DB up)
```
docker-compose run server pytest ..
```

## Database updates
```
docker-compose run server python bin/update.py
```
