cp .env.example .env
docker-compose build
docker-compose run server python bin/setup_db.py
