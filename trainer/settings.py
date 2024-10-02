# import logging
import os
import datetime
from typing import Literal
from loguru._logger import Core
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator, DirectoryPath

class Settings(BaseSettings):
    class Config:
        env_prefix = "TRAINER_"
        env_file = ".env"

    PROJECT_NAME: str = Field(
        default="trAIner",
        description="Name of the project",
    )
    LOG_LEVEL: Literal[*list(Core().levels.keys())] = Field(
        default="INFO",
        description="Logging level to be in the application",
    )
    WORK_DIR: DirectoryPath | None = Field(
        default=None,
        description=(
            "Path to the working directory. "
            "If not provided, the current directory will be used."
        )
    )
    EXPERIMENT: str | None = Field(
        default=None,
        description=(
            "Name of the experiment. "
            "It must be provided as this is used to create a "
            "directory to store the experiment results."
        )
    )
    RUN: str | None = Field(
        default=None,
        description=(
            "Name of the run. "
            "If not provided, a timestamp will be used."
        )
    )

    @field_validator("RUN")
    @classmethod
    def validate_run(cls, value):
        if value is None:
            return datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
        return value

    @field_validator("WORK_DIR")
    @classmethod
    def validate_work_dir(cls, value):
        if value is None:
            root_dir = os.path.dirname(os.path.abspath(__file__))
            work_path = os.path.join(root_dir, "../experiments")
            work_path = os.path.normpath(work_path)
            work_path = os.path.abspath(work_path)
            os.makedirs(work_path, exist_ok=True)
            return DirectoryPath(work_path)
        return value

    @property
    def run_dir(self):
        """
        Creates and returns the directory path for the current run.
        This method constructs the directory path using the WORK_DIR, EXPERIMENT,
        and RUN attributes. If the directory does not already exist, it will be created.
        Returns:
            str: The path to the run directory.
        """

        run_dir = os.path.join(self.WORK_DIR, self.EXPERIMENT, self.RUN)
        os.makedirs(run_dir, exist_ok=True)
        return run_dir

