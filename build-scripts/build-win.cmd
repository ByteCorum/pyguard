@echo off

python -m nuitka ^
    --follow-imports ^
    --remove-output ^
    --assume-yes-for-downloads ^
    --mode="onefile" ^
    --output-filename="pyguard" ^
    --windows-icon-from-ico="assets/app/icon.ico" ^
    --include-data-files="src/commands/basic/*.py=commands/basic/" ^
    --include-data-files="src/commands/obfuscation/*.py=commands/obfuscation/" ^
    --company-name="ByteCorum" ^
    --product-name="pyguard" ^
    --file-version="3.0.1.0" ^
    --product-version="3.0.1.0" ^
    --file-description="Tool/Library for Python used to obfuscate and protect your code in static and runtime from decompilation, reverse debug, etc. Also, can prevent detection by antiviruses." ^
    --copyright="https://github.com/ByteCorum/pyguard/blob/main/LICENSE" ^
    src/main.py
