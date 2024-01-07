# pablog-api

## API for handling your personal blog

### Development instruction

1) Copy **.env.example** to **.env** file. Application depends only on environment variables and this step is used
only for more convenient development.
2) Execute ```make dev-server``` It will run the uvicorn server (easy to debug).


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
1) ```make prod-server``` - locally run production version of server
2) ```make dev-server``` - run uvicorn development server
3) ```make unit-test``` - run unit tests (not in docker container)
4) ```make shell``` - run ipython interpreter with project context
5) ```make check-server-cfg``` - validate gunicorn config
6) ```make schema``` - build new openapi schema for application
7) ```make lint``` - run ruff linter
8) ```make fix``` - fix linter issues if possible
9) ```make mypy``` - run static analysis with mypy
10) ```make bandit``` - check for security issues in python code
11) ```make check-docker``` - validate docker config
12) ```make check-nginx``` - validate nginx config
13) ```make init-dev-structure``` - setup basic folders for local development. i.e logs, pid folders
14) ```make clean``` - clean trash from project


### Architecture

#### Application node architecture

![Node structure img](https://github.com/paveleroshkinweb/pablog-api/blob/main/docs/architecture/img/node.drawio.png)

Each node is a dedicated Linux virtual machine. It consists of the following parts:
1) **Nginx**
   * handle tcp connections
   * compress traffic
   * rate limit requests to protect from dos attack
   * pass api requests to application server
2) **Gunicorn**
   * communicate with nginx to accept/respond on new requests
   * supervise Uvicorn workers instances (spot/restart new instances)
3) **Uvicorn worker**
   * handle application business logic
