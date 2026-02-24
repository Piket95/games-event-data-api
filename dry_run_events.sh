#!/usr/bin/env bash

# Wait 3 minutes before running
sleep 90

# Get directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd $DIR

source .venv/bin/activate
python events.py