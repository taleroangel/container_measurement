#!/usr/bin/python3

from uuid import uuid4
from glob import glob
from shutil import rmtree
from os import path, system, makedirs

# Create and show instance UUID
INSTANCE_UUID = str(uuid4())
print(f"SingleThreadedLoad instance '{INSTANCE_UUID}'")

# Directories
IMAGES_DIRECTORY = path.normpath('./images/')
FILTERS_DIRECTORY = path.normpath('./filters/')
RESULTS_DIRECTORY = path.normpath(f'./test/results/{INSTANCE_UUID}/')

# Application executable
CLIENT = path.normpath('./src/client.py')

# Ensure file exists
assert path.exists(CLIENT), "Application executable missing"
assert path.exists(FILTERS_DIRECTORY), "Filters directory missing"
assert path.exists(IMAGES_DIRECTORY), "Images directory missing"

# Filters order
FILTERS = {
    'blur.kernel': 10,
    'gauss.kernel': 15,
    'sharp.kernel': 1,
    'sobel.kernel': 1,
    'r8.kernel': 2,
}

# Remove results if exists
if path.exists(RESULTS_DIRECTORY):
    rmtree(RESULTS_DIRECTORY)

# Create the results directory
makedirs(RESULTS_DIRECTORY)

# For each image
for image in glob(path.join(IMAGES_DIRECTORY, "*")):

    # Grab information from file
    trimmed, extension = path.splitext(image)
    base_name = path.basename(trimmed)

    # Create the result folder
    result_directory = path.join(RESULTS_DIRECTORY, base_name)
    makedirs(result_directory)

    # For each filter
    for kernel, repeats in FILTERS.items():

        # Get output file
        output_file = path.join(
            result_directory, f'{base_name}.convoluted.{kernel}{extension}')

        # Application arguments
        arguments = ["--input", image,
                     "--output", output_file,
                     "--kernel", path.join(FILTERS_DIRECTORY, kernel),
                     "--times", str(repeats)]

        # Show executable
        print(f"\nExecuting: {arguments}")

        # Build the executable
        executable = ' '.join([CLIENT, *arguments])
        # Call the executable
        result = system(executable)

        # Check if execution succeeded
        assert result == 0, f"Failed to execute client for '{image}' with '{kernel}'"

# Show instance finished
print(f"Instance '{INSTANCE_UUID}' finished")