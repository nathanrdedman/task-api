# task-api

## Introduction
This Python based REST API features methods to support CRUDs operations for managing multiple users and tasks. It also features the creation of new users, JWT based authentication to ensure permissions on tasks.

## Code
The following main Python packages were used:
- FastAPI
- SQLAlchemy (v2)
- Alembic
- Pydanitc (v2)
- Nox


## CI/CD
CI is handled via GitHub actions. Linting and typechecking is performed initially (parallel) then the main test suite is run. These can be found [here](https://github.com/nathanrdedman/task-api/actions)
Deployment has been enabled, but there is a build step to generate the API Docker image (not pushed to a repository, although I was going to push to ECR and then deploy)


## Development
To get started with developing, clone down this repository

`git clone https://github.com/nathanrdedman/task-api.git`

Create a virtual environment or miniconda environment then install in development mode

`pip install -e .[develop]`

To run the API locally we need to define a environment variable that contains the connection string. This API has been tested against SQLite and PostgreSQL. We then run the
initall migration to create the database and copy in some fixtures:

`SQLALCHEMY_DATABASE_URL="postgresql://postgres:secret@localhost:5432/postgres" alembic upgrade head`

or

`SQLALCHEMY_DATABASE_URL="sqlite:///task_api.db" alembic upgrade head`

To start the API up:

`SQLALCHEMY_DATABASE_URL="<connection+string+of+choice>" uvicorn task_api.main:app --host 0.0.0.0 --port 8080 --reload`

Navigate to [localhost:8080/docs](localhost:8080/docs) to find the automatically generated Swagger docs.

To interact with the API, you will need to authenicate. User [fixtures have been created for testing](https://github.com/nathanrdedman/task-api/blob/main/alembic/versions/961b4952e8cf_initial_tables_creation.py#L53) allowing you to authenticate and generate a JWT (automatically handled and passed the Swagger test methods). This was adapted from the FastAPI auth starter guide.

[](images/auth_button.png)

## Testing
To facilitate testing against multiple Python verisons, Nox was employed as the main runner, with two Python sessions defined (3.9, 3.10).
To run tests (after the above steps in development), call the `nox` command for the whole suite of tests or run `nox -l` to display
valid sessions, e.g.:

```
$ nox -l

Sessions defined in /home/nathan/code/task-api/noxfile.py:

* formatcheck-3.9
* formatcheck-3.10
* typecheck-3.9
* typecheck-3.10
* lint-3.9
* lint-3.10
* importscheck-3.9
* importscheck-3.10
* test-3.9
* test-3.10

sessions marked with * are selected, sessions marked with - are skipped.
```
Single sessions can be run using `nox -s <step name>`.