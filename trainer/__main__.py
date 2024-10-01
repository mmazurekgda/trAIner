import click
import sys
from loguru import logger
from trainer.settings import Settings
from pydanclick import from_pydantic
import pyfiglet as pf

@click.command(
    context_settings={"show_default": True},
)
@from_pydantic(Settings)
def cli(settings: Settings):
    logger.remove()
    logger.add(sys.stderr, level=settings.LOG_LEVEL)
    click.secho(
        pf.figlet_format(settings.PROJECT_NAME),
        fg="blue",
        bg=None,
        bold=True,
    )
    logger.info(f"Welcome to {settings.PROJECT_NAME}!")
    logger.debug(f"Applied settings: \n{settings.model_dump_json(indent=4)}")


if __name__ == "__main__":
    cli()