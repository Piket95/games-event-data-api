#!/usr/bin/env bash

if [ "$1" != "--instant" ] && [ "$1" != "--debug" ]; then
    # Wait 3 minutes before running
    echo "Waiting 3 minutes before running..."
    sleep 90
fi

# Get directory of this script
DIR="$( cd "$( dirname "$( readlink -f "${BASH_SOURCE[0]}" )" )" >/dev/null 2>&1 && pwd )"

cd $DIR

source .venv/bin/activate
python events.py $1