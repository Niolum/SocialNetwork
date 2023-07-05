# SocialNetwork
## Features

- **[FastAPI](https://fastapi.tiangolo.com/)** (Python 3.11)
  - JWT authentication using [OAuth2](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- **[PostgreSQL](https://www.postgresql.org/)** for the database
- **[SqlAlchemy](https://www.sqlalchemy.org/)** for ORM
- **[Alembic](https://alembic.sqlalchemy.org/en/latest/)** for database
  migrations
- **[Redis](https://redis.io/)** for caching likes and dislikes
- **[Pytest](https://docs.pytest.org/en/latest/)** for backend tests
- **[Docker Compose](https://docs.docker.com/compose/)**

## Quickstart

First, clone project

``` 
git clone https://github.com/Niolum/SocialNetwork.git
```

Then, create ``.env`` file. set environment variables and create database. 

Example ``.env``:

```
DATABASE_URL = "postgresql+asyncpg://username:password@localhost/db_name"
SECRET_KEY = "some secret key"
ALGORITHM = "HS256"
REDIS_URL="redis://localhost"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
TEST_DATABASE_URL = "postgresql+asyncpg://username:password@localhost/test_db_name"
CLEARBIT_API_KEY = "some api key"
CLEARBIT_URL = "https://person.clearbit.com/v2/combined/find?email="
```

Further, set up the virtual environment and the main dependencies from the ``requirements.txt``

```
python -m venv venv
source venv/bin/activate 
# or for windows
venv/Scripts/activate 
pip install -r requirements.txt
```

To run the web application in debug use:

```
alembic upgrade head
uvicorn main:app --reload
```


For start in docker-compose change ``DATABASE_URL`` and ``REDIS_URL`` in ``.env`` and start conteiners:

```
DATABASE_URL = "postgresql+asyncpg://username:some_password@backlogdb/some_name_db"
REDIS_URL="redis://redis_cache"
POSTGRES_USER=username
POSTGRES_PASSWORD=some_password
POSTGRES_DB=some_name_db
```

```
docker-compose up -d
```

## Run test

Tests for this project are defined in the tests/ folder.

To run all the tests of a project, simply run the pytest command:

```
pytest
```