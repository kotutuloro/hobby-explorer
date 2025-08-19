# Hobby Explorer

A hobby recommender service and API
(A FastAPI + ML personal practice experience, very rough, **work in progress**)

### Helpful commands

- `./bin/test <optional filename>`: runs tests
- `./bin/dev-server`: runs migrations & starts the dev server
- `./bin/dev-db`: opens a psql console into the dev database
- `./bin/seed-db`: populates hobbies table in dev database
- `./bin/generate-migration <name>`: autogenerates db migration file
- `docker-compose run migrations alembic downgrade <revision-id>`: reverts to previous db migration
- `docker-compose run migrations alembic check`: check if new db migrations would be auto-generated

### Todos:

- ML Suggestion Service
- User authentication
- Front-end
-
