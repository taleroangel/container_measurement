import base64


class BinaryFile:
    """
    Store file contents as binay file
    """

    def from_path(path):
        """
        Create from a file path
        """

        # Store contents of file in binary format
        with open(path, "rb") as image:
            # Transform to bytes array
            binary = bytearray(image.read())

        # Return the contentfile
        return BinaryFile(binary)

    def __init__(self, content: bytes | bytearray) -> None:
        self.content = content

    def store(self, path: str):
        """
        Save binary data into a file
        """
        with open(path, 'wb') as file:
            file.write(self.content)

    def decode(binary: bytes | bytearray):
        # Get content
        b64_content = binary

        # Append padding
        while len(b64_content) % 4 != 0:
            b64_content += '='

            # Create content
        return BinaryFile(
            base64.b64decode(b64_content)
        )

    def encode(self):
        return base64.b64encode(self.content).decode('ascii')
