import pprint
import typer
from models import *

app = typer.Typer()


@app.command()
def hello(payload: str):

    qg = QGen()
    output = qg.predict_mcq(payload, 3)
    typer.echo(output)


if __name__ == "__main__":
    app()
