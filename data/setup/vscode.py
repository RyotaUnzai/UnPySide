import os
import shutil
import subprocess
import threading
from pathlib import Path
from typing import Final

from cache import download_installer
from settings import global_settings
from software import AbstractSoftware, Singleton
from utils import copy_file
from vscode_settings import VSCodeConfig

BASE_DIR: Final[Path] = Path(__file__).parent
INCLUDE_DIR: Final[Path] = BASE_DIR.with_name("include")


class VSCode(AbstractSoftware, metaclass=Singleton):
    """A Singleton class that represents a VSCode instance.
    """
    __lock = threading.Lock()

    def __init__(self) -> None:
        self.__settings = global_settings.vscode

    @property
    def installed(self) -> bool:
        return self.__settings.install_dir.exists()

    def install(self) -> None:
        print("Starting setup for Visual Studio Code")
        assert not self.installed

        print(
            f"""Targets:
    Installer: {self.installer_file_name}
    Install path: {self.install_dir}
    Extensions
        """
        )
        for install_ext_file_name in self.__settings.install_extensions:
            print(f"    {install_ext_file_name}")
        print("")

        self.__install_vscode()
        self.__enable_portable_mode()
        self.__set_env()
        self.__install_extension()
        self.__uninstall_extension()
        self.__copy_user_setting()

        print("Completed setup for Visual Studio Code")

    def uninstall(self) -> None:
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
    def installer_file_name(self) -> str:
        return self.__settings.installer_file_name

    @property
    def install_dir(self) -> Path:
        return self.__settings.install_dir

    @property
    def code_cmd(self) -> Path:
        return self.__settings.code_cmd_path

    def __install_vscode(self) -> None:
        """Install VSCode
        """
        print("Installing Visual Studio Code ...")
        installer_path = download_installer(self.installer_file_name, indent_count=1)
        shutil.unpack_archive(installer_path, self.install_dir)
        print(f"Installed Visual Studio Code to '{self.install_dir}'")

    def __enable_portable_mode(self) -> None:
        """Enable VSCode portable mode

        url: https://code.visualstudio.com/docs/editor/portable#_enable-portable-mode
        """
        print("Enable VSCode portable mode")
        data_dir = self.__settings.data_dir
        os.makedirs(data_dir)
        print(f"  Created '{data_dir}'")

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
        print("Uninstall extensions")
        for uninstall_ext_id in self.__settings.uninstall_extensions:
            subprocess.run(f'"{self.code_cmd}" --uninstall-extension "{uninstall_ext_id}"', env=self.__env)

    def __copy_user_setting(self) -> None:
        """Coping settings.json
        """
        src_path = INCLUDE_DIR / "vscode-user-settings"
        dst_path = self.__settings.user_settings_path
        print("Create global settings.json")
        copy_file(src_path, dst_path, indent_count=1)
