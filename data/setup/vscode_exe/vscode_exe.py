import os
import subprocess
import sys
from pathlib import Path

LOCALAPPDATA = os.getenv("LOCALAPPDATA")
WORKSPACE_DIR = Path(sys.argv[0]).resolve().parent

def run() -> None:
    """
    Launches VSCode from the local specified in the LOCALAPPDATA environment variable with the workspace directory set
    to a directory 3 levels up from the script file location.

    Args:
        None

    Returns:
        None
    """
    vscode: Path = Path(f"{LOCALAPPDATA}/UnPySide/vscode/Code.exe")
    if vscode.exists():
        cmd = f"{vscode} {WORKSPACE_DIR}"
        p = subprocess.Popen(cmd)
    else:
        raise FileNotFoundError(f"{vscode}")


if __name__ == "__main__":
    run()
