import boto3
import io
import logging
import enum
from botocore.exceptions import ClientError
from typing import Tuple

rekognition = boto3.client('rekognition')
logging.info('Created rekognition boto3 client')

PROJECT_VERSION_ARN = 'arn:aws:rekognition:us-east-1:591083098024:project/zookeepers_polarbear/version/zookeepers_polarbear.2020-11-15T22.20.57/1605496857456'


class Label(enum.Enum):
    POLARBEAR = 'polarbear'
    NO_BEAR = 'no_bear'
    NO_RESULT = enum.auto()  # neither label met the requisite confidence level


def detect_labels(jpeg_image: io.BytesIO) -> Tuple[Label, float]:
    try:
        response: dict = rekognition.detect_custom_labels(
            ProjectVersionArn=PROJECT_VERSION_ARN,
            Image={
                'Bytes': jpeg_image.read()
            },
            MaxResults=1  # gives us the more confident of the two labels (or nothing if minimum not met)
            # MinConfidence automatically set by Rekognition based on testing results
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotReadyException':
            logging.warning('The custom labels model is not yet deployed')
            return Label.NO_RESULT, 0.
        else:  # unexpected error
            raise e

    logging.debug(f'Got response from rekognition detection: {response}')

    all_detected_labels: list = response['CustomLabels']
    if len(all_detected_labels) == 0:
        return Label.NO_RESULT, 0.

    assert len(all_detected_labels) == 1
    highest_confidence_label: dict = all_detected_labels[0]
    label_name: str = highest_confidence_label['Name']
    confidence: float = highest_confidence_label['Confidence']  # 0-100
    logging.info(f'Rekognition return label {label_name} with confidence {confidence}')
    if label_name == Label.POLARBEAR.value:
        return Label.POLARBEAR, confidence
    if label_name == Label.NO_BEAR.value:
        return Label.NO_BEAR, confidence

    logging.fatal('Unrecognized label return from rekognition')
    assert False
