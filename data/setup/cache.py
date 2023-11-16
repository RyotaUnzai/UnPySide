import os
import shutil
from pathlib import Path
from typing import Union

from settings import global_settings


def download_installer(filename: Union[str, Path], indent_count: int = 0) -> Path:
    """指定されたファイルをダウンロードしてキャッシュし、キャッシュされたファイルの完全パスを返します。
    既にキャッシュされているときは新たにダウンロードしません。
    完全パスが渡されたときは渡されたパスを何もせずそのまま返します。

    Args:
        filename: ダウンロードするファイルの名前または相対パス。
        indent_count: ログのインデント。

    Returns:
        Path: キャッシュファイルの完全パス。
    """
    if isinstance(filename, str):
        filename = Path(filename)

    # 完全パスなら何もしないでそのまま返す
    if filename.is_absolute():
        return filename

    indent = "    " * indent_count 

    # キャッシュファイルパス
    cache_file = global_settings.dev_cache_dir / filename

    # すでにキャッシュに存在すればそのまま返す
    if cache_file.exists():
        print(f"{indent}Already exists in cache '{cache_file}'")
        return cache_file
    
    # キャッシュフォルダー作成
    os.makedirs(global_settings.dev_cache_dir, exist_ok=True)

    # ダウンロード（コピー）
    src_path = global_settings.installer_dir / filename
    print(f"{indent}Downloading {src_path}")
    shutil.copyfile(src_path, cache_file)
    print(f"{indent}Downloaded {cache_file}")

    return cache_file


# DEBUG
# if global_settings.dev_cache_dir.exists():
#     shutil.rmtree(global_settings.dev_cache_dir)
