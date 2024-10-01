# import logging
from loguru import logger
from loguru._logger import Core
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Literal


class Settings(BaseSettings):
    PROJECT_NAME: str = Field(
        default="trAIner",
        description="Name of the project",
    )
    LOG_LEVEL: Literal[*list(Core().levels.keys())] = Field(
        default="INFO",
        description="Logging level to be in the application",
    )

