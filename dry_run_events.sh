#!/usr/bin/env bash

# Wait 5 minutes before running
sleep 300

# Get directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd $DIR

source .venv/bin/activate
python events.py