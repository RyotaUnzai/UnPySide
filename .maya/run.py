"""指定された Maya バージョンに対応したアプリパッケージを呼び出します。
"""
import argparse
import os
import sys
from importlib import import_module
from pathlib import Path


def run() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--space-root-dir", type=Path, required=True)
    parser.add_argument("--maya-ver", type=str, required=True)
    args = parser.parse_args()

    space_root_dir: Path = args.space_root_dir
    maya_ver: str = args.maya_ver

    print("Arguments")
    print(f"  SpaceRootDir: '{space_root_dir}'")
    print(f"  MayaVer: {maya_ver}")

    # TODO: 暫定的にここでコマンドライン引数からのスペースディレクトリ指定を環境変数にセット
    os.environ["RUNSPACE_ROOT_DIR"] = str(space_root_dir)

    # アプリパッケージ呼び出しのためにソースコードフォルダーを sys.path に追加
    source_path = space_root_dir / "src"
    print(f"Add to sys.path '{source_path}'")
    sys.path.append(str(source_path))

    # アプリパッケージのインポート
    app_pkg_path = f"Core.Maya{maya_ver}"
    print(f"Import '{app_pkg_path}'")
    app_module = import_module(app_pkg_path)

    app_launcher = app_module.AppLauncher(space_root_dir)

    app_launcher.launch()


if __name__ == "__main__":
    run()
