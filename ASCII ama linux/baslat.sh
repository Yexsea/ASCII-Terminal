#!/usr/bin/env bash
# Sanal ortamdaki Python ile programı çalıştır
cd "$(dirname "$0")"

if [ ! -x venv/bin/python ]; then
    echo "Önce kurulumu çalıştır: bash kurulum.sh"
    exit 1
fi

exec venv/bin/python ASCII.py "$@"
