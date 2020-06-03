cp .env.example .env
docker-compose up --no-start
docker-compose run server python bin/db_ingest.py --years 2020 --rows 500
docker-compose up
