import json
import os

from pablog_api.api.server import VERSION
from pablog_api.api.server import app as server

import typer

from fastapi.openapi.utils import get_openapi


app = typer.Typer()


@app.command(
    name="schema",
    help="Command to generate a fresh openapi schema based on app routes"
)
def generate_schema():
    schema = json.dumps(get_openapi(
        title="PablogAPI",
        version=VERSION,
        description="PablogAPI openapi specification",
        routes=server.routes,
    ))
    filepath = os.path.join(os.getcwd(), "docs", "schema", "openapi.json")
    with open(filepath, "w") as file:
        file.write(schema)
        file.flush()


@app.command()
def check():
    pass
