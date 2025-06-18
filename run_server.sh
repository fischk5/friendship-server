#!/bin/bash

VENV_DIR="venv"
python -m venv $VENV_DIR  

if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    echo "Detected Linux/macOS."
    ACTIVATE_PATH="$VENV_DIR/bin/activate"
elif [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "cygwin"* || ("$OSTYPE" == "win32" && -n "$MSYSTEM") ]]; then
    echo "Detected Windows (Bash-like environment)."
    ACTIVATE_PATH="$VENV_DIR/Scripts/activate"
else
    echo "Unsupported operating system: $OSTYPE. Cannot determine activation script."
    exit 1
fi

source $ACTIVATE_PATH

pip install -r requirements.txt  
python server.py