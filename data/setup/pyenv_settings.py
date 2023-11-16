from pathlib import Path
from pydantic import Field
from config import AbstractConfig


class PyenvConfig(AbstractConfig):
    version: str = Field(alias="Version")
    """software version"""
    install_dir: Path = Field(alias="InstallDir")
    """installation directory of the software"""
