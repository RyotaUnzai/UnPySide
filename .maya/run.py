import os
import sys
from argparse import ArgumentParser
from importlib import import_module
from pathlib import Path
from typing import Any

from typing_extensions import Self


class Maya:
    parser: ArgumentParser
    args: Any

    def __init__(self: Self):
        self.__set_parser()

    def __set_parser(self: Self):
        self.parser = ArgumentParser()
        self.parser.add_argument("--root-dir", type=Path, required=True)
        self.parser.add_argument("--dcc-name", type=str, required=True)
        self.parser.add_argument("--dcc-version", type=str, required=True)
        self.args = self.parser.parse_args()

    @property
    def root_dir(self: Self) -> Path:
        return self.args.root_dir

    @property
    def dcc_name(self: Self) -> str:
        return self.args.dcc_name

    @property
    def dcc_version(self: Self) -> str:
        return self.args.dcc_version

    @property
    def source_dir(self: Self) -> Path:
        return self.root_dir / "lib"

    @property
    def dcc_package_path(self: Self) -> Path:
        return f"DCC.{self.dcc_name}.{self.dcc_name}{self.dcc_version}"

    def __set_env(self: Self) -> None:
        os.environ["UNPYSIDE_ROOT_DIR"] = str(self.root_dir)

    def __add_sys_path(self: Self) -> None:
        print(f"Add to sys.path '{self.source_dir}'")
        sys.path.append(str(self.source_dir))

    def __check_arguments(self: Self) -> None:
        print("Arguments")
        print(f"  SpaceRootDir: '{self.root_dir}'")
        print(f"  DCCName: '{self.root_dir}'")
        print(f"  Ver: {self.dcc_version}")

    def __import_modules(self: Self) -> import_module:
        print(f"Import '{self.dcc_package_path}'")
        return import_module(self.dcc_package_path)

    def run(self: Self) -> None:
        self.__set_env()
        self.__check_arguments()
        self.__add_sys_path()

        dcc_modules = self.__import_modules()
        dcc_launcher = dcc_modules.Launcher(self.root_dir)
        dcc_launcher.launch()


if __name__ == "__main__":
    maya = Maya()
    maya.run()
