import typer
import uvicorn

from popug_sdk.conf import settings


def runserver(
    host: str = typer.Option("0.0.0.0"),
    port: int = typer.Option(settings.app.app_port),
    debug: bool = typer.Option(False),
    reload: bool = typer.Option(False),
    workers: int = typer.Option(1),
) -> None:
    uvicorn.run(
        settings.app.instance,
        host=host,
        port=port,
        debug=debug,
        reload=reload,
        workers=workers,
    )
