import json
import os

from pablog_api.api import app as server
from pablog_api.settings.app import get_app_settings

import typer

from fastapi.openapi.utils import get_openapi


app = typer.Typer()

settings = get_app_settings()


@app.command(
    name="stub",
)
def _():
    pass


@app.command(
    name="schema",
    help="Command to generate a fresh openapi schema based on app routes"
)
def generate_schema():
    schema = json.dumps(get_openapi(
        title=settings.app_name,
        version=settings.app_version,
        description="Openapi specification",
        routes=server.routes,
    ))
    filepath = os.path.join(os.getcwd(), "docs", "openapi-schema", f"openapi_{settings.app_version}.json")
    with open(filepath, "w") as file:
        file.write(schema)
        file.flush()
