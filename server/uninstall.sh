# not working yet
# docker system prune -a --volumes
# docker rmi postgres -f
# docker volume rm orchestration_backend_data

docker-compose kill

# remove all images
docker rmi -f 311_data_server
docker rmi -f 311_data_redis
docker rmi -f adminer
docker rmi -f postgres
docker rmi -f marian/rebrow
docker rmi -f redis
docker rmi -f python

# remove the volume
docker volume rm -f 311_data_database

# remove the network
docker network rm 311_data_default
