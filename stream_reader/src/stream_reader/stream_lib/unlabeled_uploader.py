import boto3
import io
import logging
import random
import time

UNLABELED_BUCKET_NAME = 'zookeepers-unlabled'
UNLABELED_TEST_DATA_BUCKET_NAME = 'zookeepers-unlabeled-testdata'
TEST_DATA_PERCENT = .2  # percentage of images which are used as test data

s3 = boto3.client('s3')


def upload_image(jpeg_bytes: io.BytesIO, stream_id: str) -> None:
    bucket = UNLABELED_BUCKET_NAME
    if random.random() < TEST_DATA_PERCENT:
        bucket = UNLABELED_TEST_DATA_BUCKET_NAME

    s3.upload_fileobj(jpeg_bytes, bucket, f'{stream_id}/{int(time.time())}.jpeg')
    logging.info(f'Successfully uploaded new image to {bucket}')
