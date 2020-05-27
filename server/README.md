

## Setup

1. Install docker, docker-compose and git

2. copy server/.env.example to server/.env and add a SOCRATA_TOKEN

3. Seed your local DB

```
docker-compose run server python bin/ingest.py
```

4. Start devving

```
docker-compose up --build
```

## Running tests

docker-compose run server pytest ..

## Linting

docker-compose run server flake8 ..

## Database updates

```
docker-compose run server python bin/update.py
```
