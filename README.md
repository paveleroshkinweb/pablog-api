# pablog-api

## API for handling your personal blog

### Technology Stack
* [FastAPI](https://fastapi.tiangolo.com/) for the Python backend API.
* [Nginx](https://nginx.org/) as a webserver
* [PostgreSQL](https://www.postgresql.org/) as master database
* [Docker](https://www.docker.com/) for testing/development/production.
* [Pytest](https://docs.pytest.org/en/8.2.x/) for smoke/unit/integration tests

### Development instruction

1) Download tools that you need for local development: [poetry](https://python-poetry.org/), [docker](https://www.docker.com/)
2) Run ```poetry install --with dev``` to install dev dependencies. i.e linter, static analyzer
3) Run ```make init-dev-structure``` to setup basic folders for local development. i.e logs, pid
4) Run ```make server``` It will run the server and all required services in docker.

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
2) Tests CI
   * unit tests


### Development commands
#### CI
1) ```make unit-test``` - run unit tests (not in docker container)
2) ```make check-server-cfg``` - validate gunicorn config
3) ```make schema``` - export new openapi schema into docs/openapi-schema/openapi_VERSION.json
4) ```make lint``` - run ruff linter
5) ```make lint-fix``` - fix linter issues if possible
6) ```make mypy``` - run static analysis with mypy
7) ```make bandit``` - check for security issues in python code
8) ```make check-docker``` - validate docker config
9) ```make check-nginx``` - validate nginx config

#### LOCAL DEVELOPMENT
1) ```make server``` - locally run production version of server
2) ```make stop-server``` - stops local cluster
3) ```make py-shell``` - run ipython interpreter with project context
4) ```make c-bash``` - run bash interpreter inside of docker container
5) ```make migrations``` - create migrations based on new models updates
6) ```make migrate``` - migrate database to latest revision

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
