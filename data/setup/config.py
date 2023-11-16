from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, validator
from utils import resolve_env_path


class Validator:
    @classmethod
    def path_validator(cls, name: str) -> Any:
        """Create a validator for a given name that ensures the value is a valid path.

        This validator checks if the provided value is of type `Path`. It it is,
        It attempts to resolve any environment variables present in the path using
        the `resolve_env_path` function.

        Args:
            name : The name associated with the validator.

        Returns:
            Any: A validator function.

        Raise:
            ValueError: If the resolution of environment variables in the path fails.
        """
        def _validate_path(value: Any) -> Path | None:
            """Validates if the input is a Path type and resolves environment variables.

            Args:
                value: The input value to validate and potentially transform.

            Returns:
                Path | None: The resolved path if input is of type Path, otherwise the original value.

            Raises:
                ValueError: If the resolution of environment variables in the path fails.
            """
            if isinstance(value, Path):
                return resolve_env_path(value)
            return value
        print("path_validator")
        r = validator(name, allow_reuse=True)(_validate_path)
        return r


class AbstractConfig(BaseModel):
    """Abstract base class representing a configuration.

    Provides common properties and methods that can be shared across
    different configuration implementations. It should not be instantiated
    directly but should be subclassed.

    Attributes:
        _path_validator: A class-level path validator for ensuring proper path format.
    """
    _path_validator = Validator.path_validator("*")
    print("AbstractConfig")


class AbstractSoftWareConfig(AbstractConfig):
    """Abstract base class representing software-specific configuration.

    Contains attributes common to software configurations, such as version and
    installation directory. As with `AbstractConfig`, this class is meant to be
    subclassed and should not be instantiated directly.

    Attributes:
        _version: Version of the software.
        _install_dir: Installation directory for the software.

    Properties:
        version: Returns the version of the software.
        install_dir: Returns the installation directory of the software.
    """
    _version: str = Field(alias="Version")
    _install_dir: Path = Field(alias="InstallDir")

    def __init__(self, *args, **kwargs):
        super(AbstractSoftWareConfig, self).__init__(*args, **kwargs)

    @property
    def version(self) -> str:
        """Get the software version."""
        return self._version

    @property
    def install_dir(self) -> Path:
        """Get the installation directory of the software."""
        return self._install_dir
