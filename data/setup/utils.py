import os
import re
import shutil
from pathlib import Path
from typing import Union


def resolve_env_path(path: Union[str, Path]) -> Path:
    """Resolves a given path by expanding any environment variables it contains.

    This function tales a path which might contain environment variables
    (in the form of `%VAR%` or `%VAR`) and returns a new `Path` object with
    those variables expanded to their respective values.

    Args:
        path: THe input path that might contain environment variables.

    Raises:
        RuntimeError: if unable to expand the environment variables within the Path.

    Returns:
        Path: A new `Path` object with all environment variables expanded.
 
    Example:
    >>> resolve_env_path("%USERPROFILE%/Desktop")
    Path("C:/Users/YourUsername/Desktop")

    Note:
    This function repeatedly attempts to expand environment variables
    until the path remains unchanged, or until all environment variables are
    fully expanded.
    """
    if isinstance(path, Path):
        path = str(path)

    while "%" in path or "$" in path:
        prev = path
        path = os.path.expandvars(path)
        if path == prev:
            raise RuntimeError(
                f"Unable to expand environment variables. '{path}'"
            )

    return Path(path)


def copy_file(src: Union[str, Path], dst: Union[str, Path], indent_count: int = 1) -> None:
    indent = "    " * indent_count
    print(f"{indent}CopyFile from '{src}' to '{dst}'")
    shutil.copyfile(src, dst)


class Guard:
    @staticmethod
    def is_not_none_or_whitespace(s: str) -> str:
        # None または空文字のとき例外をスローします
        assert isinstance(s, str)
        assert s is not None or len(str.strip(s)) > 0
        return s

    @staticmethod
    def is_whitespace_free(s: str) -> str:
        # None または空文字のとき、および空白文字を含むとき例外をスローします
        assert isinstance(s, str)
        assert s is not None or len(str.strip(s)) > 0
        assert not re.match(r"^.*\s.*$", s), "空白文字が含まれています"
        return s
