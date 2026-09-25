#!/bin/bash

python -m nuitka \
    --follow-imports \
    --remove-output \
    --mode="app" \
    --assume-yes-for-downloads \
    --output-filename="pyguard" \
    --linux-icon="assets/app/icon.png" \
    --include-package="src/commands" \
    --follow-import-to="src/commands" \
    --include-data-files="src/commands/obfuscation/obfuscate.py=commands/obfuscation/obfuscate.py" \
    --include-data-files="src/commands/obfuscation/obfuscatelegacy.py=commands/obfuscation/obfuscatelegacy.py" \
    --include-data-files="src/commands/basic/help.py=commands/basic/help.py" \
    --include-data-files="src/commands/basic/info.py=commands/basic/info.py" \
    --include-data-files="src/commands/basic/dependencies.py=commands/basic/dependencies.py" \
    --linux-app-license="GPL v3" \
    --company-name="ByteCorum" \
    --product-name="pyguard" \
    --file-version="3.0.1.0" \
    --product-version="3.0.1.0" \
    --file-description="Tool/Library for Python used to obfuscate and protect your code in static and runtime from decompilation, reverse debug, etc. Also, can prevent detection by antiviruses." \
    --copyright="https://github.com/ByteCorum/pyguard/blob/main/LICENSE" \
    src/main.py
