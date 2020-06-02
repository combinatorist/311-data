

## Setup

1. Install docker, docker-compose and git

2. clone this repo and `cd` into the `server` directory

3. copy .env file: `cp .env.example .env`

4. add socrata token to .env file

5. build your containers: `docker-compose build`

6. Seed your local DB: `docker-compose run server python bin/ingest.py`


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
