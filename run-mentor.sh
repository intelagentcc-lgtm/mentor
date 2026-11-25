#!/bin/sh
set -eu

cd "$(dirname "$0")"

if [ ! -x .venv/bin/python ]; then
    if ! command -v python3 >/dev/null 2>&1; then
        printf '%s\n' "Install Python 3, then run this launcher again." >&2
        exit 1
    fi
    printf '%s\n' "Creating Mentor’s Python environment…"
    python3 -m venv .venv
fi

if ! cmp -s requirements.txt .venv/mentor-requirements.txt; then
    printf '%s\n' "Installing Mentor’s document dependencies…"
    .venv/bin/python -m pip --disable-pip-version-check install -r requirements.txt
    cp requirements.txt .venv/mentor-requirements.txt
fi

exec .venv/bin/python server.py "$@"
