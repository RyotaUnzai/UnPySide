from pathlib import Path

from pydantic import Field

from data.setup.config import AbstractSoftWareConfig


class VSCodeConfig(AbstractSoftWareConfig):
    _installer_file_name: str = Field(alias="InstallerFileName")
    install_extensions: list[str] = Field(alias="InstallExtensions")
    uninstall_extensions: list[str] = Field(alias="UninstallExtensions")

    @property
    def installer_file_name(self) -> str:
        return f"{self._installer_file_name}{self.version}.zip"

    @property
    def data_dir(self) -> Path:
        return self.install_dir / "data"

    @property
    def code_cmd_path(self) -> Path:
        return self.install_dir / "bin\\code.cmd"

    @property
    def user_settings_path(self) -> Path:
        return self.install_dir / "data\\user-data\\User\\settings.json"
