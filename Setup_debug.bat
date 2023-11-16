@echo off
chcp 65001 > nul
cd /d %~dp0
setlocal enabledelayedexpansion

call:rmdir "%~dp0.venv\Include"
call:rmdir "%~dp0.venv\Lib"
call:rmdir "%~dp0.venv\Lib-Dev"
call:rmdir "%~dp0.venv\Scripts"
call:del "%~dp0.venv\pyenv.cfg"

set PYENV=%LOCALAPPDATA%\UnPySide\pyenv\pyenv-win
set PYENV_ROOT=%LOCALAPPDATA%\UnPySide\pyenv\pyenv-win
set PYENV_HOME=%LOCALAPPDATA%\UnPySide\pyenv\pyenv-win
set PATH=%LOCALAPPDATA%\UnPySide\pyenv\pyenv-win\bin;%LOCALAPPDATA%\UnPySide\pyenv\pyenv-win\shims;%PATH%

powershell -NoProfile -ExecutionPolicy Unrestricted %~dp0data\setup\setup-env.ps1
call "%LOCALAPPDATA%\UnPySide\python\tools\python.exe" -B "%~dp0data\setup\setup.py"

call "%LOCALAPPDATA%\UnPySide\pyenv\pyenv-win\bin\pyenv.bat" install 3.9.7
call "%LOCALAPPDATA%\UnPySide\pyenv\pyenv-win\shims\python.bat" -B -m venv .venv
call %~dp0.venv\Scripts\activate.bat

python -m pip install -r "%~dp0data\requirements.txt"
@REM python -m pip install -r "%~dp0data\requirements_dev.txt" --target "%~dp0.venv\Lib-Dev\site-packages"

:rmdir
if exist %1 rmdir /s /q %1
exit /b

:del
if exist %1 del %1