"""
Code responsible for pulling an image (the provided stream preview image) from the San Diego zoo livestream.
"""
import requests
import logging
import io
import imghdr


def get_jpeg_at_url(url: str) -> bytes:
    logging.debug(f'Called with {url}')
    r = requests.get(url)
    if not (r.status_code < 300):
        raise ConnectionError(f'Response from {url} was not <300, got {r.status_code}')
    if imghdr.what(io.BytesIO(r.content)) != 'jpeg':
        raise ValueError(f'Content retrieved from {url} was not a JPEG image')
    logging.info(f'Successfully retrieved JPEG image from {url}')
    return r.content
