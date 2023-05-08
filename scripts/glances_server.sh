#!/usr/bin/env sh

glances -w -p 24112 &
python3 ./scripts/server.py
