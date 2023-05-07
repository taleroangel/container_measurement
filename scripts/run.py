#!/usr/bin/python3

import glob
from shutil import rmtree, copytree, move
from os import path, system, makedirs, remove

# Directories
IMAGES_DIRECTORY = path.normpath('./images/')
FILTERS_DIRECTORY = path.normpath('./filters/')
RESULTS_DIRECTORY = path.normpath('./results/')

# Application executable
APPLICATION = path.normpath('./build/apply_convolution')

# Ensure file exists
assert path.exists(APPLICATION), "Application executable missing"
assert path.exists(FILTERS_DIRECTORY), "Filters directory missing"
assert path.exists(IMAGES_DIRECTORY), "Images directory missing"

# Filters order
FILTERS = {
    'blur.kernel': 10,
    'gauss.kernel': 10,
    'sharp.kernel': 1,
    'sobel.kernel': 1,
    'r8.kernel': 2,
}

# Remove results if exists
if path.exists(RESULTS_DIRECTORY):
    rmtree(RESULTS_DIRECTORY)

# Copy contents
copytree(IMAGES_DIRECTORY, RESULTS_DIRECTORY)

# For each filter apply convolution
for kernel, repeats in FILTERS.items():

    # Output extension
    kernel_name = kernel.split('.')[0]
    output_extension = f".{kernel_name}.jpg"

    # Application arguments
    arguments = ["--input", RESULTS_DIRECTORY, "--extension", ".jpg",
                 "--output", output_extension, "--kernel", path.join(FILTERS_DIRECTORY, kernel), "--repeat", str(repeats)]

    # Create executable
    executable = [APPLICATION, *arguments]

    # Run executable
    command = ' '.join(executable)
    print(command)
    system(command)

    # Copy contents to folder
    directory_path = path.join(RESULTS_DIRECTORY, kernel_name)
    makedirs(directory_path)

    # Match files with extension
    output_directory = f'{RESULTS_DIRECTORY}/*{output_extension}'
    print(f'Reading directory for: {output_directory}')

    # Move contents to folder
    for file in glob.glob(output_directory):
        move(file, directory_path)

# Remove remaining paths
for file in glob.glob(f'{RESULTS_DIRECTORY}/*.jpg'):
    remove(file)
