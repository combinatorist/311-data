## Getting Started

### TL;DR
  - install docker and docker compose on your machine
  - run `chmod +x install.sh && ./install.sh` from this directory
  - put a Socrata token in your `.env` file, and run `docker-compose run server python bin/db_seed.py --years 2019,2020`

### Step 1 of 3: install docker and docker-compose
Docker and Docker-Compose are the only required dependencies for running the server. They're both  available on all platforms. You can find installation instructions [here](https://docs.docker.com/compose/install/) for Docker and [here](https://docs.docker.com/compose/install/) for Docker-Compose. (The two come bundled together for Mac and Windows, which makes things pretty easy.)

Once you're done, you can check that everything is working by running these commands:
```
docker --version           // confirms docker is installed
docker-compose --version   // confirms docker-compose is installed
docker info                // confirms the docker daemon is running
```

### Step 2 of 3: run the install script
With docker running on your machine, `cd` into this directory and run:
```
chmod +x install.sh && ./install.sh
```
This will download a bunch of docker images, set up your database, and then fire everything up. If all goes well, at the end you should have running api server backed by Postgres and Redis.

If you'd like to take a tour of the services and make sure everything works, you can then visit these URLs:
- http://localhost:5000 -- the api -- should say that the api is running
- http://localhost:8080 -- postgres GUI -- should show you the database. Login with the following:
  - System: **PostgreSQL**
  - Server: **db**
  - Username: **311_user**
  - Password: **311_pass**
  - Database: **311_db**
- http://localhost:5001 -- redis GUI -- lets you inspect the contents of Redis.
  - In the Host box, change 'localhost' to 'redis' and then hit Connect to log in.

`Ctrl-C` will shut down the server and all supporting services. And `docker-compose up` will bring everything back up again.

### Step 3 of 3: seed your database
Right now the server is functional and all endpoints should be working. But for most purposes you'll need some data in your database. The data comes from [Socrata](https://dev.socrata.com/), a public api that hosts many datasets for LA and other cities. To add data, you'll need to get a Socrata token and run one more command.

- #### Step 3a (maybe optional): add a Socrata token to your .env file
Socrata threatens to throttle you if you don't have an api token. We're not sure they actually do that, but if you want to be sure, get a token from another team member or [register](https://opendata.socrata.com/login) with Socrata and they'll give you one. Then add it to the Socrata section in your `.env` file:
```
SOCRATA_TOKEN=thetoken
```
- #### Step 3b: run the seed script
It takes a while to seed the database, so we recommend starting with 2 years of data from Socrata. Run the following command to get data for 2019 and 2020, which is plenty for most dev purposes. ETA **20 to 30 minutes**.
```
docker-compose run server python bin/db_seed.py --years 2019,2020
```
On the other hand, if you want your local DB to match production, and you've got some time, you can drop the `--years` flag. The following command will download all available data from Socrata (2015 through 2020). ETA **60 to 90 minutes**.
```
docker-compose run server python bin/db_seed.py
```
Run one of these commands and get some coffee. When it's done, you'll be ready to start developing.

(NOTE: This is not a huge decision, because you can download years in separate commands. For example, if you run the first command above to get 2019 and 2020, you can later run `docker-compose run server python bin/db_seed.py --years 2015,2016,2017,2018` to get the rest of Socrata's data.

For more info on the seed command, run  `docker-compose run server python bin/db_seed.py --help`.

Also, if you ever want to reset your DB and start over, run `docker-compose run server python bin/db_reset.py`)


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
The following command will remove all docker containers, images, volumes, and networks that are specific to this project.
```
docker-compose down --rmi local --volumes
```
