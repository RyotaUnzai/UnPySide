from pathlib import Path

from pydantic import Field

from config import AbstractConfig


class UnPySideEnvConfig(AbstractConfig):
    interpreter_path: Path = Field(alias="InterpreterPath")
