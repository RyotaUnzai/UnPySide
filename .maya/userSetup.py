import os
from pathlib import Path
from typing import Final

from Core import EnvironmentVariableKey
from Core.proxy_print import register

DEBUGGER_PORT: Final[int] = 5678

if EnvironmentVariableKey.CAT_DEBUGGER_ENABLE in os.environ:
    import debugpy

    mayapy_exe = Path(os.environ["MAYA_LOCATION"], "bin", "mayapy.exe")
    debugpy.configure(python=mayapy_exe.as_posix())

    debugpy.connect(DEBUGGER_PORT)


register()

try:
    # TODO: 展開されているアプリパッケージを動的にインポートするように変更が必要
    # TODO: そもそも起動の起点は Workspace である
    from Core.Maya2023.bootstrap import bootstrap

    bootstrap()
except Exception as ex:
    debugpy.breakpoint()
    print(ex)
