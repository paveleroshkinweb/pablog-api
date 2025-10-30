# pablog-api

## API for handling your personal blog

### Technology Stack
* [FastAPI](https://fastapi.tiangolo.com/) for the Python backend API.
* [Nginx](https://nginx.org/) as a webserver
* [SQLite](https://sqlite.org/) as master database
* [Redis](https://redis.io/) as cache service
* [Docker](https://www.docker.com/) for testing/development/production.
* [Pytest](https://docs.pytest.org/en/8.2.x/) for smoke/unit/integration tests

### Development instruction

1) Download tools that you need for local development: [poetry](https://python-poetry.org/), [docker](https://www.docker.com/)
2) Run ```poetry install --with dev``` to install dev dependencies. i.e linter, static analyzer
3) Run ```make init-dev-structure``` to setup basic folders for local development. i.e logs, pid
4) Run ```make start-cluster``` It will run the server and all required services in docker.

All application/nginx/database logs can be found in logs folder.

Now you can open your browser and interact with these URLs:
* Backend, JSON based web API based on OpenAPI: http://localhost:8001/api/v1
* Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost:8001/docs/openapi

Note: The first time you start your stack, it might take a minute for it to be ready. While the backend waits for the database to be ready and configures everything. You can check the logs to monitor it.

### CI

For CI the github actions and pre-commit was used. All workflows you can find [here](https://github.com/paveleroshkinweb/pablog-api/tree/main/.github/workflows).
It includes 2 main workflows:
1) Base CI 
   * linter
   * mypy
   * gunicorn config validation
   * python code security check
   * docker config validation


### Development commands
#### CI
1) ```make schema``` - export new openapi schema into docs/openapi-schema/openapi_VERSION.json
2) ```make lint``` - run ruff linter
3) ```make lint-fix``` - fix linter issues if possible
4) ```make mypy``` - run static analysis with mypy

#### LOCAL DEVELOPMENT
1) ```make start-cluster``` - locally run production version of cluster
2) ```make stop-cluster``` - stops local cluster
3) ```make logs``` - shows logs for all cluster processes
4) ```make connect service={service_name}``` - run bash interpreter inside of docker container service
5) ```make stop service={service_name}``` - stop the service
6) ```make pyshell``` - run ipython interpreter with project context
7) ```make dbshell``` - run psql terminal command for master database
8) ```make redishell``` - run redis-cli terminal
9) ```make migrations name={custom_name}``` - create migrations based on new models updates
10) ```make drop-migrations``` - drops all alembic migrations information from database.
11) ```make migrate rev={revision_id}``` - migrate database to particular revision. leave empty (```make migrate```) if want to update to latest revision
12) ```make rollback``` - rollback last applied migration from database
13) ```make check-migrations``` - checks if required migrations generated or not. it's integrated into pre-commit hook

#### UTILS
1) ```make init-dev-structure``` - setup basic folders for local development. i.e logs, pid folders
2) ```make clean``` - clean trash from project (logs, docker containers)


### Architecture

#### Application node architecture

![Node structure img](https://github.com/paveleroshkinweb/pablog-api/blob/main/docs/architecture/img/node.drawio.png)

Each node is a dedicated Linux virtual machine. It consists of the following parts:
1) **Nginx**
   * handle tcp connections
   * compress traffic
   * pass api requests to application server
2) **Gunicorn**
   * communicate with nginx to accept/respond on new requests
   * supervise Uvicorn workers instances (spot/restart new instances)
3) **Uvicorn worker**
   * handle application business logic
