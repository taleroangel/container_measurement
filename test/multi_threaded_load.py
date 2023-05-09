#!/usr/bin/python3

from os import path, system
import argparse
import threading

parser = argparse.ArgumentParser(
    description="Make multiple threaded request")

# Add arguments to parser
parser.add_argument('-n', '--number', type=int,
                    help="Number of concurrent threads", required=True)

# Get arguments
ARGUMENTS = parser.parse_args()
SINGLE_THREADED_LOAD = path.normpath('./test/single_threaded_load.py')

# Build the threadpool
thread_pool: list[threading.Thread] = [threading.Thread(
    target=lambda: system(SINGLE_THREADED_LOAD)) for _ in range(ARGUMENTS.number)]

# Start threads
for t in thread_pool:
    t.start()

# Join threads
for t in thread_pool:
    t.join()
