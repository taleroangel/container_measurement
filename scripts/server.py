#!/usr/bin/python3

import socket
import signal
import pickle
import threading
import content
import os
import uuid

# Define host and port
HOST = 'localhost'
PORT = 24111

# Directories
RUN_DIRECTORY = os.path.normpath('./run/')
RESULTS_DIRECTORY = os.path.join(RUN_DIRECTORY, 'results')
EXECUTABLE = os.path.normpath('./build/apply_convolution')


class InterruptionHandler():
    def __init__(self) -> None:
        # Check if interupted
        self.is_interrupted = False

        # Register signal handler
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, *args):
        print("Recieved interruption")
        self.is_interrupted = True


def client_handler(connection: socket.socket, address):
    # Print information
    print(f"\n[{threading.current_thread().name}] New connection from: {address}")

    # Read size
    data_size = connection.recv(6, socket.MSG_WAITALL)
    data_size = int.from_bytes(data_size, 'little', signed=False)
    # Read data
    serialized_content = connection.recv(data_size, socket.MSG_WAITALL)
    assert len(
        serialized_content) == data_size, f"Content[{len(serialized_content)}] and Size[{data_size}] do not match"

    # Deserialize object
    deserialized_request: content.ContentRequest = pickle.loads(
        serialized_content)

    # Get response
    response = request_handler(deserialized_request)
    # Serialize the response
    response_bytes = pickle.dumps(response)

    # Send size
    content_size = len(response_bytes).to_bytes(6, 'little', signed=False)
    connection.send(content_size, socket.MSG_MORE)
    # Send the response
    connection.sendall(response_bytes)

    # Close the connection
    connection.close()

    # Print and exit
    print(f"Finished processing: [{threading.current_thread().name}]\n")
    exit(0)


def request_handler(request: content.ContentRequest) -> content.ContentResponse:
    # Store the image in the run directory
    image_file = os.path.join(RUN_DIRECTORY, request.input.name)

    # Check if exists and delete it
    if os.path.exists(image_file):
        os.remove(image_file)

    # Create the file
    os.makedirs(os.path.dirname(image_file), exist_ok=True)

    # Write contents to file
    request.input.store(image_file)

    # Write kernel
    kernel_file = os.path.join(RUN_DIRECTORY, request.kernel.name)

    # Check if exists and delete it
    if os.path.exists(kernel_file):
        os.remove(kernel_file)

    # Create the file
    os.makedirs(os.path.dirname(kernel_file), exist_ok=True)

    # Write contents to file
    request.kernel.store(kernel_file)

    # Get the file basename
    _, file_extension = os.path.splitext(image_file)
    random_uuid = str(uuid.uuid4())

    # build output filename
    output_filename = os.path.join(
        RESULTS_DIRECTORY, (random_uuid + file_extension))

    # prepare arguments
    arguments = [
        "--input", image_file,
        "--output", output_filename,
        "--kernel", kernel_file,
        "--times", str(request.times),
        "--grayscale" if request.grayscale else ""
    ]

    os.system(' '.join([EXECUTABLE, *arguments]))

    # Return the response
    return content.ContentResponse(content.ContentFile(output_filename))


# Application entry point
if __name__ == "__main__":

    # Check executable
    assert os.path.exists(EXECUTABLE), "apply_convolution executable missing"

    # Ensure directory exists
    if not os.path.exists(RUN_DIRECTORY):
        os.makedirs(RUN_DIRECTORY)

    if not os.path.exists(RESULTS_DIRECTORY):
        os.makedirs(RESULTS_DIRECTORY)

    # Create a socket object
    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    SOCKET.bind((HOST, PORT))

    # Listen for incoming connections
    SOCKET.listen(10)

    # Set non blocking IO
    SOCKET.setblocking(False)

    # Show information about the server
    print(f"Server is listening on {HOST}:{PORT}")

    # Create the interruption handler
    interruption = InterruptionHandler()

    # Client threads
    threads: list[threading.Thread] = []

    # Main loop
    while not interruption.is_interrupted:
        try:
            # Accept a new connection
            connection, address = SOCKET.accept()

            # Create thread
            thread = threading.Thread(
                name=str(uuid.uuid4()),
                target=client_handler,
                args=(connection, address))

            # Add it to threads
            threads.append(thread)
            thread.start()

        except BlockingIOError:
            continue

        # Check dead threads
        for t in threads:
            # Check if thread is not alive
            if not t.is_alive():
                t.join()
                threads.remove(t)
                print(f"Removing dead thread: [{t.name}]")

    # Wait for all threads
    for thread in threads:
        thread.join()

    # Close the socket
    SOCKET.close()
    print("Server finished...")
