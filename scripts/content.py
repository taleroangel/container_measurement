class ContentFile:
    def __init__(self, name) -> None:
        self.name = name

        with open(name, "rb") as image:
            file = image.read()
            self.content = bytearray(file)

    def store(self, output=None):
        if output is None:
            output = self.name

        with open(output, 'wb') as file:
            file.write(self.content)

    def __str__(self) -> str:
        return f"File[{self.name}, size:{len(self.content)}]"


class ContentRequest:
    def __init__(self, input: ContentFile, kernel: ContentFile, times: int, grayscale: bool) -> None:
        self.input = input
        self.kernel = kernel
        self.times = times
        self.grayscale = grayscale

    def __str__(self) -> str:
        return f"Request[\n\tinput: {self.input}\n\tkernel: {self.kernel}\n\ttimes: {self.times}\n\tgrayscale: {self.grayscale}\n]"


class ContentResponse:
    def __init__(self, output: ContentFile) -> None:
        self.output = output

    def __str__(self) -> str:
        return f"Response[\n\toutput: {self.output}\n]"
