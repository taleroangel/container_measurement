import cv2
import numpy as np


def convolute_image(image: np.ndarray, kernel: np.ndarray, times: int) -> np.ndarray:
    """
    Create convolution of image
    """

    # Copy image
    image_convolution = image.copy()
    # Convolute n times
    for _ in range(times):
        image_convolution = cv2.filter2D(image_convolution, -1, kernel)

    # Return convolution
    return image_convolution


def list_to_kernel(content: list[float]) -> np.ndarray:
    """
    Parse kernel in list form to numpy array
    """
    return np.array(content)


def bytes_to_image(image: bytes, grayscale: bool) -> np.ndarray:
    """
    Decode image bytes to opencv image
    """
    buffer = np.frombuffer(image, np.uint8)
    return cv2.imdecode(buffer, cv2.IMREAD_GRAYSCALE if grayscale else cv2.IMREAD_COLOR)


def image_to_bytes(image: np.ndarray, extension: str):
    """
    Encode opencv image into bytes
    """
    success, buffer = cv2.imencode(ext=extension, img=image)
    assert success, "Failed to encode image"
    return buffer
