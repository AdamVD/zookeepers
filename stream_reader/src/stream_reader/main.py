"""
Entry-point for the zookeeper's container.
"""

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s')

import time
from stream_lib import image_from_url
from stream_lib import sns_notifications

URL_REPLACE_STR = 'STREAM_ID'
SAN_DIEGO_PREVIEW_IMAGE_URL_TEMPLATE = f'https://{URL_REPLACE_STR}.preview.api.camzonecdn.com/previewimage'
LOOP_SLEEP_S = 10


class STREAM_IDS:
    POLAR_BEAR = 'polarplunge'


def forever_loop(stream_id: str) -> None:
    while True:
        # the preview image updates at something like a 7-8 second interval
        logging.debug('Loop begin')
        time.sleep(LOOP_SLEEP_S)
        try:
            jpeg_bytes = image_from_url.get_jpeg_at_url(SAN_DIEGO_PREVIEW_IMAGE_URL_TEMPLATE.replace(URL_REPLACE_STR, stream_id))
        except ConnectionError as e:
            logging.error(e)
            logging.info('Will continue to next loop after error')
        except ValueError as e:
            logging.error(e)
            logging.info('Will continue to next loop after error')

        sns_notifications.send_notification(sns_notifications.AnimalStatus.NOT_VISIBLE)


if __name__ == '__main__':
    logging.info('Zookeeper application start')
    forever_loop(STREAM_IDS.POLAR_BEAR)
