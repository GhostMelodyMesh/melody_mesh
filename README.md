# melody_mesh
Music recommendation software, which uses user's Spotify, SoundCloud and YouTube.


# Linux setup
sudo snap install docker

# Running the app on Linux
- sudo docker-compose up --build              // on requirements.txt, Dockerfile or compose.yaml change
- sudo docker-compose run -it melody-app /bin/bash
- python ./src/main.py


# Windows setup
Download Docker Desktop and run it

# Running the app on Windows
- docker-compose up --build                   // on requirements.txt, Dockerfile or compose.yaml change
- docker-compose run -it melody-app /bin/bash
- python ./src/main.py


# Running tests
pytest


# New running
docker compose --profile local-db run --service-ports --rm melody-app bash