#!/bin/bash

python -m nuitka \
    --follow-imports \
    --remove-output \
    --mode="onefile" \
    --assume-yes-for-downloads \
    --output-filename="pyguard" \
    --linux-icon="assets/app/icon.png" \
    --include-data-files="src/commands/basic/*.py=commands/basic/" \
    --include-data-files="src/commands/obfuscation/*.py=commands/obfuscation/" \
    --linux-app-license="GPL v3" \
    --company-name="ByteCorum" \
    --product-name="pyguard" \
    --file-version="3.0.1.0" \
    --product-version="3.0.1.0" \
    --file-description="Tool/Library for Python used to obfuscate and protect your code in static and runtime from decompilation, reverse debug, etc. Also, can prevent detection by antiviruses." \
    --copyright="https://github.com/ByteCorum/pyguard/blob/main/LICENSE" \
    src/main.py
