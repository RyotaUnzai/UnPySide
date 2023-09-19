from pathlib import Path
from typing import Final

from pyenv import Pyenv
from vscode import VSCode
BASE_DIR: Final[Path] = Path(__file__).parent


if __name__ == "__main__":
    vscode = VSCode()
    pyenv = Pyenv()

    vscode.uninstall()
    pyenv.uninstall()

    vscode.install()
    pyenv.install()
