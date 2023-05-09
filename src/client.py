#!/usr/bin/python3


from colorama import Back, Fore, Style
import argparse
import json
from os import path

import requests as http
import binary as bn
import request as rq


def read_kernel(path: str) -> list[float]:
    """
    Read a convolution kernel file
    """

    # Empty kernel
    kernel: list[float] = []

    # Open file and read its lines
    with open(path) as f:
        lines = f.readlines()

    # For each line
    for i in range(len(lines)):

        # Parse it to numbers
        line = lines[i].strip().split()

        # For each number in line
        for j in range(len(line)):

            # Add it to the kernel
            kernel.append(float(line[j]))

    return kernel


def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(
        description="Send an image to be convoluted in a remote server")

    # Add arguments to parser
    parser.add_argument('-a', '--address', type=str,
                        help="Address of the remote server", default='localhost')
    parser.add_argument('-p', '--port', type=int,
                        help="Port of the remote server", default=24111)
    parser.add_argument('-i', '--input', type=str,
                        help="Input image to be convoluted", required=True)
    parser.add_argument('-o', '--output', type=str,
                        help="Output image path", required=True)
    parser.add_argument('-k', '--kernel', type=str,
                        help="Kernel file to use", required=True)
    parser.add_argument('-t', '--times', type=int,
                        help="Number of times to repeat the convolution", default=1)
    parser.add_argument('-g', '--grayscale', action='store_true',
                        help="Open the image as a grayscale")

    # Parse arguments
    print(Back.YELLOW + f"ApplyConvolution Client - @taleroangel" + Style.RESET_ALL)
    ARGUMENTS = parser.parse_args()

    # Show connection
    print(f'Attempting connection to: [{ARGUMENTS.address}:{ARGUMENTS.port}]')

    # Grab the extension
    _, extension = path.splitext(ARGUMENTS.input)

    # Create request
    request = rq.ContentRequest(
        # Input File
        bn.BinaryFile.from_path(
            path.normcase(ARGUMENTS.input)),
        # Kernel from file
        read_kernel(
            path.normcase(ARGUMENTS.kernel)),
        # File extension
        extension,
        # Other parameters
        ARGUMENTS.times, ARGUMENTS.grayscale)

    # Serialize content into json
    payload = json.dumps(request.to_dict())
    headers = {'Content-Type': 'application/json'}

    # Make request
    print(Fore.YELLOW +
          f"💡 Sending request to server ({len(payload)} bytes)", Style.RESET_ALL)

    # HTTP request
    try:
        response = http.post(f'http://{ARGUMENTS.address}:{ARGUMENTS.port}/',
                             data=payload, headers=headers)
    except:
        print(Back.RED +
              f"🧩 Request failed (Request timed out)", Style.RESET_ALL)
        exit(1)

    # Get the response
    if (response.status_code != 200):
        print(Fore.WHITE + Back.RED +
              f"🧩 Request failed, response from server: {response.status_code}",
              Style.RESET_ALL)
        # Error, exit
        exit(2)

    print(Fore.YELLOW + f"⚡️ Recieved server response ({len(response.text)} bytes)",
          Style.RESET_ALL)

    # Serialize into file
    response_content = bn.BinaryFile.decode(response.text)
    response_content.store(ARGUMENTS.output)

    # Print file
    print(Fore.GREEN +
          f"Result stored in: '{ARGUMENTS.output}'" + Style.RESET_ALL)


# Call from main
if __name__ == '__main__':
    main()
