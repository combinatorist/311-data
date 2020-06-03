cp .env.example .env
docker-compose build
docker-compose run server python bin/db_create.py
