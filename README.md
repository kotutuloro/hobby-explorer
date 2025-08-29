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
  - handle key errors
  - use content-based recommendation system when there's not enough user data
  - use the hobby.interested column in similarity analysis
  - save and load analysis to/from feather files
  - cron job recreates analysis from sql every hour?
- User authentication
- Front-end
-
