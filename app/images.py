"""Image logic: loading an image and describing it."""

from io import BytesIO
from pathlib import Path

import httpx
from PIL import Image, UnidentifiedImageError

# Refuse larger images: the whole file is loaded in memory
MAX_IMAGE_BYTES = 10 * 1024 * 1024


class ImageLoadError(Exception):
    """Raised when an image cannot be read from the given path or URL."""


def load_image_bytes(source: str) -> bytes:
    """Read an image from a local path or download it from an http(s) URL."""

    # Paths copied from a file manager may come wrapped in quotes
    source = source.strip().strip("\"'")

    if source.startswith(("http://", "https://")):
        try:
            response = httpx.get(source, follow_redirects=True, timeout=10)
            response.raise_for_status()
        except httpx.HTTPError as error:
            raise ImageLoadError(f"Could not download '{source}': {error}") from error
        data = response.content
    else:
        try:
            data = Path(source).expanduser().read_bytes()
        except OSError as error:
            raise ImageLoadError(
                f"Could not read the file '{source}' ({error.strerror}). "
                "Ask the user for the absolute path of the image."
            ) from error

    if len(data) > MAX_IMAGE_BYTES:
        raise ImageLoadError(
            f"The image is too large ({len(data)} bytes; "
            f"the limit is {MAX_IMAGE_BYTES} bytes)."
        )

    return data


def describe_image(source: str) -> dict:
    """Describe the image at a local path or URL: format, size, color mode, DPI."""

    data = load_image_bytes(source)

    try:
        image = Image.open(BytesIO(data))
    except UnidentifiedImageError as error:
        raise ImageLoadError(f"'{source}' is not an image file.") from error

    # Not every file stores its resolution: when it is missing, we report `None`
    dpi = image.info.get("dpi")

    return {
        "format": image.format,
        "mime_type": Image.MIME.get(image.format),
        "width": image.width,
        "height": image.height,
        "mode": image.mode,
        "dpi": [round(float(value)) for value in dpi] if dpi else None,
        "size_bytes": len(data),
    }
