echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

call %1\%2
call nuitka --msvc=14.3 --standalone --onefile --disable-console -o "Code" %1\%3\vscode_exe\vscode_exe.py --windows-icon-from-ico=%1\%3\resources\vscode.ico --output-dir=%1\%3\vscode_exe --plugin-enable=pylint-warnings --plugin-enable=tk-inter --windows-disable-console --windows-product-name="VSCode" --windows-file-description="Launch VSCode to deploy the UnPySide workspace environment." --windows-product-version=1.0.3 --windows-company-name="UnPySide"
move %1\%3\vscode_exe\Code.exe %1\Code.exe 