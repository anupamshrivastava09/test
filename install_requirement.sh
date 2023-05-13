#!/usr/bin/bash

python_path="/opt/python3.7.7/bin"

venv="/Czentrix/apps/tts_fastapi/venv"

$python_path/python3 -m venv $venv

$venv/bin/pip install --upgrade pip
$venv/bin/pip install -r tts_requirement.txt

