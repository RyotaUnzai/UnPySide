import os
from pathlib import Path

import yaml
from pydantic import Field, validator
from pydantic.fields import ModelField

from config import AbstractConfig
from pyenv_settings import PyenvConfig
from unpysidepy_settings import UnPySideEnvConfig
from vscode_settings import VSCodeConfig

os.environ["WORK_SPACE_FOLDER"] = Path(__file__).parent.parent.parent.as_posix()


class Settings(AbstractConfig):
    env_dir: Path = Field(alias="UnPySideDir")
    dev_dir: Path = Field(alias="UnPySideDir")
    dev_cache_dir: Path = Field(..., alias="UnPySideCacheDir")
    installer_dir: Path = Field(alias="InstallerDir")

    unpysidepy: UnPySideEnvConfig = Field(alias="UnPySidepy")
    vscode: VSCodeConfig = Field(alias="VSCode")
    pyenv: PyenvConfig = Field(alias="Pyenv")

    @validator("*")
    def __register_environment_variable(cls, v, values: dict, config, field: ModelField, **kwargs):
        # ルート直下の Path クラスにバインドするフィールドを環境変数に登録
        # pydantic により自動で呼び出されます
        print(v)
        if isinstance(v, Path):
            os.environ[field.alias] = str(v)
        return v

# TODO:
with open(Path(__file__).parent / "setup-settings.yml") as file:
    obj = yaml.safe_load(file)

global_settings: Settings = Settings.parse_obj(obj)
