from pyenv import Pyenv
from vscode import VSCode

if __name__ == "__main__":
    vscode = VSCode()
    pyenv = Pyenv()

    vscode.uninstall()
    pyenv.uninstall()

    vscode.install()
    pyenv.install()
