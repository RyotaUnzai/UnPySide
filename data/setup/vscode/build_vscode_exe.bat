echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

call %1\%2
call nuitka --standalone --onefile --disable-console -o "Code" %1\%3\vscode\vscode_exe.py --windows-icon-from-ico=%1\%3\resources\vscode.ico --output-dir=%1\%3\vscode
move %1\%3\vscode\Code.exe %1\Code.exe
