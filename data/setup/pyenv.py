import os
import shutil
import subprocess
import threading
from pathlib import Path
from typing import Self
from logging import Logger

from settings import global_settings
from utils import Guard


class Pyenv:
    """A Singleton class that represents a Pyenv instance.
    """
    __lock = threading.Lock()

    def __new__(cls, *args, **kwargs) -> Self:
        if not hasattr(cls, "_instance"):
            with cls.__lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(Pyenv, cls).__new__(cls)

        return cls._instance

    def __init__(self,  logger: Logger) -> Self:
        self.__logger = logger
        self.__settings = global_settings
        settings = self.__settings.pyenv
        self.__install_dir = install_dir = settings.install_dir

        self.__version = Guard.is_not_none_or_whitespace(settings.version)
        self.__pywin_dir = install_dir / "pyenv-win"
        self.__bin_dir = self.__pywin_dir / "bin"
        self.__shims_dir = self.__pywin_dir / "shims"
        self.__pyenv_bat = self.__bin_dir / "pyenv.bat"
        self.__python_bat = self.__shims_dir / "python.bat"

    @property
    def installed(self) -> bool:
        return self.__install_dir.exists()

    def install(self) -> None:
        assert not self.installed

        install_dir = self.__install_dir

        self.__logger.info(f"Installing pyenv in '{install_dir}")

        # pyenv-win のインストール
        subprocess.run(
            f'"{self.__settings.unpysidepy.interpreter_path}" -m pip install pyenv-win=={self.__version} --target "{self.__install_dir}'
        )

        self.__logger.info(f"Installed pyenv in '{install_dir}")

    def uninstall(self) -> None:
        install_dir = self.__install_dir

        if not install_dir.exists():
            self.__logger.info(f"Skipped uninstall pyenv because not installed '{install_dir}'")
            return

        self.__logger.info(f"Uninstalling pyenv from '{install_dir}'")

        shutil.rmtree(install_dir)

        self.__logger.info(f"Uninstalled pyenv from '{install_dir}'")

    def apply_environ(self, environ: dict[str, str] | None = None) -> dict[str, str]:
        assert self.installed

        if environ is None:
            environ = os.environ.copy()

        environ["PYENV"] = environ["PYENV_ROOT"] = environ["PYENV_HOME"] = str(self.__pywin_dir)
        environ["PATH"] = str(self.__bin_dir) + ";" + str(self.__shims_dir) + ";" + environ["PATH"]

        return environ

    def install_python(self, py_ver: str) -> None:
        # 指定バージョンの Python を pyenv にインストール

        assert self.installed
        Guard.is_not_none_or_whitespace(py_ver+"  ")

        self.__logger.info(f"Installing Python {py_ver} into pyenv")

        env = self.apply_environ()

        subprocess.run(f'"{self.__pyenv_bat}" install {py_ver}', env=env)

        self.__logger.info(f"Installed Python {py_ver} into pyenv")

    def uninstall_python(self, py_ver: str) -> None:
        # 指定バージョンの Python を pyenv からアンインストール

        assert self.installed
        Guard.is_not_none_or_whitespace(py_ver)

        self.__logger.info(f"Uninstalling Python {py_ver} from pyenv")

        env = self.apply_environ()

        subprocess.run(f'"{self.__pyenv_bat}" uninstall {py_ver}', env=env)

        self.__logger.info(f"Uninstalled Python {py_ver} from pyenv")

    def create_env(self, target_dir: Path, py_ver: str) -> None:
        assert self.installed
        assert target_dir.is_absolute()
        Guard.is_not_none_or_whitespace(py_ver)

        self.install_python(py_ver)

        env = self.apply_environ()
        prev_cwd = os.getcwd()
        os.chdir(target_dir)
        try:
            subprocess.run(f'"{self.__pyenv_bat}" local {py_ver}', env=env)

            # create venv
            subprocess.run(f'"{str(self.__python_bat)}" -B -m venv .venv', env=env)

            # Disable warnings to update pip for use in virtual environments
            with open(target_dir / ".venv" / "pip.ini", "w", encoding="utf-8") as f:
                f.write("[global]\ndisable-pip-version-check = True")
        finally:
            os.chdir(prev_cwd)
