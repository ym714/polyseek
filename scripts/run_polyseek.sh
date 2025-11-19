#!/bin/bash
# Polyseek execution script

cd "$(dirname "$0")"
export PYTHONPATH="src:$PYTHONPATH"

if [ "$1" = "--offline" ]; then
    export POLYSEEK_OFFLINE=1
    shift
fi

python3 -c "
import sys
sys.path.insert(0, 'src')
from polyseek_sentient.main import _run_cli
import asyncio
import json

url = sys.argv[1] if len(sys.argv) > 1 else 'https://polymarket.com/event/test'
depth = sys.argv[2] if len(sys.argv) > 2 else 'quick'
perspective = sys.argv[3] if len(sys.argv) > 3 else 'neutral'

asyncio.run(_run_cli(url, depth, perspective))
" "$@"
