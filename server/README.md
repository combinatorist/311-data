## Getting Started

### TL;DR
  - install docker and docker compose on your machine
  - `chmod +x install.sh && ./install.sh`
  - put a [Socrata](https://dev.socrata.com/) api token in the `.env` file
  - `docker-compose run server python bin/db_seed.py --years 2019,2020`

### Step 1: install docker and docker-compose
Docker and Docker-Compose are the only required dependencies for running the server. They're both  available on all platforms. You can find installation instructions [here](https://docs.docker.com/compose/install/) for Docker and [here](https://docs.docker.com/compose/install/) for Docker-Compose. (The two come bundled together for Mac and Windows, which makes things pretty easy.)

Once you're done, you can check that everything is working by running these commands:
```
docker --version           // confirms docker is installed
docker-compose --version   // confirms docker-compose is installed
docker info                // confirms the docker daemon is running
```

### Step 2: run the install script
With docker running on your machine, `cd` into this directory and run:
```
chmod +x install.sh && ./install.sh
```
This will download/build a bunch of docker images, create your `.env` file, set up your database, and then fire everything up. If all goes well, at the end you should have running api server backed by Postgres and Redis.

If you'd like to take a tour of the services and make sure everything works, you can then visit these URLs:
- http://localhost:5000 -- the api -- should say "you hit the index". This means the api is running.
- http://localhost:8080 -- postgres GUI -- lets you inspect the database. Login with the following:
  - System: **PostgreSQL**
  - Server: **db**
  - Username: **311_user**
  - Password: **311_pass**
  - Database: **311_db**
- http://localhost:5001 -- redis GUI -- lets you inspect the contents of Redis.
  - In the Host box, change 'localhost' to 'redis' and then hit Connect to log in.

`Ctrl-C` will shut down the server and all supporting services. And `docker-compose up` will bring everything back up again.

### Step 3: seed your database
Right now the server is functional and all endpoints should be working. But for most purposes you'll need some data in your database. The data comes from [Socrata](https://dev.socrata.com/), a public api that hosts many datasets for LA and other cities. To add data, you'll need to get a Socrata token and run one more command.

- #### Step 3a (possibly optional): add a Socrata token to your .env file
Socrata threatens to throttle you if you don't have an api token. We're not sure they actually do that, but the api does seem to run more slowly without a token. So get a token from another team member, or [register](https://opendata.socrata.com/login) with Socrata and they'll give you one. Then add it to the Socrata section in your `.env` file:
```
SOCRATA_TOKEN=thetoken
```
- #### Step 3b: run the seed script
It takes a while to seed the database, so we recommend starting with 2 years of data from Socrata. Run the following command to get data for 2019 and 2020, which is plenty for most dev purposes. ETA **20 to 30 minutes**.
```
docker-compose run server python bin/db_seed.py --years 2019,2020
```
If you decide later that you need more data, just run the command again with the year(s) you want to add. Socrata goes back to 2015.

(NOTE: run the above command with `--help` instead of `--years` for more info on the options. And if you ever want to reset your database and start over, run `docker-compose run server python bin/db_reset.py`.)


## Development
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


## Uninstall
The following command will remove all docker containers, images, volumes, and networks that are specific to this project. It will leave in place generic docker assets (like the `postgres` and `python` images) that you may be using for other purposes.
```
docker-compose down --rmi local --volumes
```
