from pathlib import Path
from typing import Final

from logging import getLogger, basicConfig
from rich.logging import RichHandler

from pyenv import Pyenv
from vscode import VSCode

BASE_DIR: Final[Path] = Path(__file__).parents


if __name__ == "__main__":
    FORMAT = "%(message)s"
    basicConfig(
        level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    )
    logger = getLogger("rich")

    vscode = VSCode(logger)
    vscode.uninstall()
    vscode.install()

    pyenv = Pyenv(logger)
    pyenv.uninstall()
    pyenv.install()

