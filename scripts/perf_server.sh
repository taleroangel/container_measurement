#!/usr/bin/env sh

# perf record the script
perf record -g --sample-cpu ./scripts/server.py