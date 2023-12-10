import typer
import uvicorn

app = typer.Typer()


@app.command()
def runserver():
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)  # type: ignore


@app.command()
def makemigrations():
    from subprocess import run

    run(["alembic", "revision", "--autogenerate", "-m", "init"], check=True)


@app.command()
def migrate():
    from subprocess import run

    run(["alembic", "upgrade", "head"], check=True)


if __name__ == "__main__":
    app()
