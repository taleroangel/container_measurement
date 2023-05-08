#!/usr/bin/python3
import socket
import argparse
import pickle
import content
import os

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
ARGUMENTS = parser.parse_args()

# Create request
request = content.ContentRequest(
    content.ContentFile(os.path.normcase(ARGUMENTS.input)),  # Input File
    content.ContentFile(os.path.normcase(ARGUMENTS.kernel)),  # Output File
    ARGUMENTS.times, ARGUMENTS.grayscale)

# Serialized object
serialized = pickle.dumps(request)

# Create socket
CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to remote server
CLIENT_SOCKET.connect((ARGUMENTS.address, ARGUMENTS.port))
print("Connection to server established")

# Show the request
print(request)

# Send size
content_size = len(serialized).to_bytes(6, 'little', signed=False)
CLIENT_SOCKET.send(content_size, socket.MSG_MORE)
print(f"ContentSize (bytes) sent: {len(serialized)} [{len(content_size)}]")

# Send content
CLIENT_SOCKET.sendall(serialized)
print("Request was sent to the Server")

# Read size
data_size = CLIENT_SOCKET.recv(6, socket.MSG_WAITALL)
data_size = int.from_bytes(data_size, 'little', signed=False)
print(f"DataSize (bytes): {data_size}")

# Read data
serialized_content = CLIENT_SOCKET.recv(data_size, socket.MSG_WAITALL)
assert len(
    serialized_content) == data_size, f"Content[{len(serialized_content)}] and Size[{data_size}] do not match"


# Close connection
CLIENT_SOCKET.close()

# Deserialize object
deserialized_response: content.ContentResponse = pickle.loads(
    serialized_content)

# Show response
print(deserialized_response)

# Store it
deserialized_response.output.store(ARGUMENTS.output)

print("Closed connection with server")
print(f"Result stored in: {ARGUMENTS.output}")
