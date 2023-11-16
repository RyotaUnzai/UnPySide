from pathlib import Path

from pydantic import Field

from config import AbstractConfig


class VSCodeConfig(AbstractConfig):
    version: str = Field(alias="Version")
    """software version"""
    install_dir: Path = Field(alias="InstallDir")
    """installation directory of the software"""
    workspace_dir: Path = Field(alias="WorkSpaceDir")
    """workspace directory full path"""
    installer_file_base_name: str = Field(alias="InstallerFileName")
    """installation file name"""
    install_extensions: list[str] = Field(alias="InstallExtensions")
    """installation Extensions"""
    uninstall_extensions: list[str] = Field(alias="UninstallExtensions")
    """Uninstallation Extensions"""

    @property
    def installer_file_full_path(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return f"{self.installer_file_base_name}-{self.version}.zip"

    @property
    def data_dir(self) -> Path:
        """_summary_

        Returns:
            Path: _description_
        """
        return self.install_dir / "data"

    @property
    def code_cmd_path(self) -> Path:
        """Code 

        Returns:
            Path: _description_
        """
        return self.install_dir / "bin\\code.cmd"

    @property
    def user_settings_path(self) -> Path:
        """_summary_

        Returns:
            Path: _description_
        """
        return self.install_dir / "data\\user-data\\User\\settings.json"

    @property
    def workspace_preference_dir(self) -> Path:
        """_summary_

        Returns:
            Path: _description_
        """
        return self.workspace_dir / ".vscode"

    @property
    def workspace_settings_path(self) -> Path:
        """_summary_

        Returns:
            Path: _description_
        """
        return self.workspace_preference_dir / "settings.json"

    @property
    def workspace_code_workspace_path(self) -> Path:
        """_summary_

        Returns:
            Path: _description_
        """
        return self.workspace_preference_dir / "unpyside.code-workspace"

    @property
    def workspace_cspell_path(self) -> Path:
        """_summary_

        Returns:
            Path: _description_
        """
        return self.workspace_preference_dir / "cspell.json"

    @property
    def workspace_pyproject_path(self) -> Path:
        """_summary_

        Returns:
            Path: _description_
        """
        return self.workspace_dir / "pyproject.toml"

