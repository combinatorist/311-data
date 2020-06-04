## Getting Started

### Step 1 of 3: install docker and docker-compose
Docker/Docker-Compose are the only required dependencies for running the server. They are available on all platforms. You can find installation instructions [here](https://docs.docker.com/compose/install/) for Docker and [here](https://docs.docker.com/compose/install/) for Docker-Compose. (The two come bundled together for Mac and Windows, which makes things pretty easy.)

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

`Ctrl-C` will shut down all of these services. And `docker-compose up` will bring them all back up again.

### Step 3 of 3: seed your database
Right now the server is functional and all endpoints should be working. But for most purposes you'll need some data in your database. The data comes from [Socrata](https://dev.socrata.com/), a public api that hosts many datasets for LA and other cities. To add data, you'll need to get a Socrata token and run one more command.

- #### Step 3a (maybe optional): add a Socrata token to your .env file
Socrata threatens to throttle you if you don't have an api token. We're not sure they actually do that, but if you want to be sure, get a token from another team member or [register](https://opendata.socrata.com/login) with Socrata and they'll give you one. Then add it to the Socrata section in your `.env` file:
```
SOCRATA_TOKEN=thetoken
```
- #### Step 3b: run the seed script
It takes a while to seed the database, so we recommend starting with 2 years of data from Socrata. The ETA for this command is 20 to 30 minutes.
```
docker-compose run server python bin/db_seed.py --years 2019,2020
```
If you want your local DB to match production, you can drop the `--years` flag. This will download all available data from Socrata -- 2015 through 2020. ETA 60 to 90 minutes.
```
docker-compose run server python bin/db_seed.py
```
Run one of these commands and get some coffee. When it's done, you'll be ready to start developing.

(NOTE: You can also download years in succession. For example, running `docker-compose run server python bin/db_seed.py --years 2019` followed by `docker-compose run server python bin/db_seed.py --years 2018,2020` would add three years to your DB. Run `docker-compose run server python bin/db_seed.py --help` for more info on the seed command.

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
