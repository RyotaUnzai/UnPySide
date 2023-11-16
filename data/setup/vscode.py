import os
import shutil
import subprocess
import threading
from pathlib import Path
from typing import Final, Self
from logging import Logger

from software import AbstractSoftware, Singleton
from cache import download_installer
from settings import global_settings
from utils import copy_file
from vscode_settings import VSCodeConfig

BASE_DIR: Final[Path] = Path(__file__).parent
INCLUDE_DIR: Final[Path] = BASE_DIR.with_name("include")


class VSCode:
    """A Singleton class that represents a VSCode instance.
    """

    __lock = threading.Lock()

    def __init__(self, logger: Logger) -> Self:
        self.__logger = logger
        self.__settings = global_settings.vscode

    def __new__(cls, *args, **kwargs) -> Self:
        # Singleton
        if not hasattr(cls, "_instance"):
            # Thread-safe
            with cls.__lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(VSCode, cls).__new__(cls)
        return cls._instance

    @property
    def installed(self) -> bool:
        return self.__settings.install_dir.exists()

    def install(self) -> None:
        self.__logger.info("Starting setup for Visual Studio Code")
        assert not self.installed

        self.__logger.info(
            f"""Targets:
    Installer: {self.installer_file_full_path}
    Install path: {self.install_dir}
    Extensions
        """
        )
        for install_ext_file_name in self.__settings.install_extensions:
            self.__logger.info(f"    {install_ext_file_name}")
        self.__logger.info("")

        self.__install_vscode()
        self.__enable_portable_mode()
        self.__set_env()
        self.__install_extension()
        self.__uninstall_extension()
        self.__copy_user_setting()
        self.__copy_workspace_setting()

        self.__logger.info("Completed setup for Visual Studio Code")

    def uninstall(self) -> None:
        self.__logger.info(self.__settings)
        install_dir = self.__settings.install_dir
        if install_dir.exists():
            shutil.rmtree(install_dir)

    @property
    def settings(self) -> VSCodeConfig:
        """_summary_

        Returns:
            VSCodeConfig: _description_
        """
        return self.__settings

    @property
    def installer_file_full_path(self) -> str:
        return self.__settings.installer_file_full_path

    @property
    def install_dir(self) -> Path:
        return self.__settings.install_dir

    @property
    def code_cmd(self) -> Path:
        return self.__settings.code_cmd_path

    def __install_vscode(self) -> None:
        """Install VSCode
        """
        self.__logger.info("Installing Visual Studio Code ...")
        installer_path = download_installer(self.installer_file_full_path, indent_count=1)
        shutil.unpack_archive(installer_path, self.install_dir)
        self.__logger.info(f"Installed Visual Studio Code to '{self.install_dir}'")

    def __enable_portable_mode(self) -> None:
        """Enable VSCode portable mode

        url: https://code.visualstudio.com/docs/editor/portable#_enable-portable-mode
        """
        self.__logger.info("Enable VSCode portable mode")
        data_dir = self.__settings.data_dir
        os.makedirs(data_dir)
        self.__logger.info(f"  Created '{data_dir}'")

    def __set_env(self):
        """Set Environment Variables

        Note: (node:8824) [DEP0005] DeprecationWarning: Buffer() is deprecated due to security and usability issues.
                Please use the Buffer.alloc(), Buffer.allocUnsafe(), or Buffer.from() methods instead.
        """
        self.__env = os.environ.copy()
        self.__env["NODE_OPTIONS"] = "--no-deprecation"

    def __install_extension(self) -> None:
        """Install extension
        """
        for extension in self.__settings.install_extensions:
            subprocess.run(f'"{self.code_cmd}" --install-extension "{extension}" --force', env=self.__env)

    def __uninstall_extension(self) -> None:
        """Uninstall extension
        """
        self.__logger.info("Uninstall extensions")
        for uninstall_ext_id in self.__settings.uninstall_extensions:
            subprocess.run(f'"{self.code_cmd}" --uninstall-extension "{uninstall_ext_id}"', env=self.__env)

    def __copy_user_setting(self) -> None:
        """Coping settings.json
        """
        src_path = INCLUDE_DIR / "vscode-user-settings"
        dst_path = self.__settings.user_settings_path
        self.__logger.info("Create global setting")
        copy_file(src_path, dst_path, indent_count=1)

    def __copy_workspace_setting(self) -> None:
        """Coping settings.json
        """
        self.__logger.info("Create workspace setting")
        self.__logger.info(self.__settings.workspace_preference_dir)
        if self.__settings.workspace_preference_dir.exists():
            shutil.rmtree(self.__settings.workspace_preference_dir)
        os.makedirs(self.__settings.workspace_preference_dir)

        copy_file(INCLUDE_DIR / "settings", self.__settings.workspace_settings_path, indent_count=1)
        self.__logger.info(" Created cspell")
        copy_file(INCLUDE_DIR / "cspell", self.__settings.workspace_cspell_path, indent_count=1)
        self.__logger.info(" Created code-workspace")
        copy_file(INCLUDE_DIR / "code-workspace", self.__settings.workspace_code_workspace_path, indent_count=1)
        self.__logger.info(" Created settings")
        copy_file(INCLUDE_DIR / "pyproject", self.__settings.workspace_pyproject_path, indent_count=1)
        self.__logger.info(" Created pyproject")
