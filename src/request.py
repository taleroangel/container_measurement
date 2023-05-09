import binary as bn


class ContentRequest:
    """
    Serialized content request
    """

    def __init__(self,
                 input: bn.BinaryFile,
                 kernel: list[float],
                 extension: str,
                 times: int,
                 grayscale: bool) -> None:
        
        self.input = input
        self.kernel = kernel
        self.extension = extension
        self.times = times
        self.grayscale = grayscale

    def to_dict(self):
        return {
            "input": self.input.encode(),
            "kernel": self.kernel,
            "extension": self.extension,
            "times": self.times,
            "grayscale": self.grayscale
        }

    def from_dict(dict):
        return ContentRequest(
            bn.BinaryFile.decode(dict['input']),
            list(dict['kernel']),
            str(dict['extension']),
            int(dict['times']),
            bool(dict['grayscale'])
        )
