"""指定された Maya バージョンに対応したアプリパッケージを呼び出します。
"""
import argparse
import os
import sys
from importlib import import_module
from pathlib import Path


def run() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root-dir", type=Path, required=True)
    parser.add_argument("--dcc-name", type=str, required=True)
    parser.add_argument("--dcc-version", type=str, required=True)
    args = parser.parse_args()

    root_dir: Path = args.root_dir
    dcc_name: str = args.dcc_name
    dcc_version: str = args.dcc_version

    print("Arguments")
    print(f"  SpaceRootDir: '{root_dir}'")
    print(f"  DCCName: '{dcc_name}'")
    print(f"  Ver: {dcc_version}")

    os.environ["UNPYSIDE_ROOT_DIR"] = str(root_dir)

    source_path = root_dir / "lib"
    print(f"Add to sys.path '{source_path}'")
    sys.path.append(str(source_path))

    dcc_package_path = f"DCC.{dcc_name}.{dcc_name}{dcc_version}"
    print(f"Import '{dcc_package_path}'")
    dcc_modules = import_module(dcc_package_path)
    dcc_launcher = dcc_modules.Launcher(root_dir)
    dcc_launcher.launch()


if __name__ == "__main__":
    run()
