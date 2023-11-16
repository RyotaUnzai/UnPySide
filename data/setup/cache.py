import os
import shutil
from pathlib import Path
from typing import Union

from settings import global_settings


def download_installer(filename: Union[str, Path], indent_count: int = 0) -> Path:
    """Downloads and caches the specified file, returning the full path to the cached file.

    If the file is already cached, it will not be downloaded again.
    If a full path is provided, it simply returns the given path without any action.

    Args:
        filename : The filename or path of the file to download.
        indent_count : The level of indentation for the output. Default is 0.

    Returns:
        Path: The full path to the downloaded (or already cached) file.

    """
    if isinstance(filename, str):
        filename = Path(filename)

    if filename.is_absolute():
        return filename

    indent = "    " * indent_count 

    cache_file = global_settings.dev_cache_dir / filename

    if cache_file.exists():
        print(f"{indent}Already exists in cache '{cache_file}'")
        return cache_file

    os.makedirs(global_settings.dev_cache_dir, exist_ok=True)

    src_path = global_settings.installer_dir / filename
    print(f"{indent}Downloading {src_path}")
    shutil.copyfile(src_path, cache_file)
    print(f"{indent}Downloaded {cache_file}")

    return cache_file


# DEBUG
# if global_settings.dev_cache_dir.exists():
#     shutil.rmtree(global_settings.dev_cache_dir)
