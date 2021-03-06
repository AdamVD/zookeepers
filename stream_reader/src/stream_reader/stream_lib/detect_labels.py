import boto3
import io
import os
import logging
import enum
from botocore.exceptions import ClientError
from typing import Tuple

rekognition = boto3.client('rekognition', region_name=os.environ['REGION'])
logging.info('Created rekognition boto3 client')

PROJECT_VERSION_ARN = os.environ['REKOGNITION_MODEL_ARN']
started_project_version = False


class Label(enum.Enum):
    POLARBEAR = 'polarbear'
    NO_BEAR = 'no_bear'
    NO_RESULT = enum.auto()  # neither label met the requisite confidence level


def start_project_version() -> None:
    logging.info(f'Starting the desired Custom Labels project version')
    try:
        response: dict = rekognition.start_project_version(
            ProjectVersionArn=PROJECT_VERSION_ARN,
            MinInferenceUnits=1
        )
        logging.info(f'Got response {response} from rekognition')
        assert response['Status'] == 'STARTING' or response['Status'] == 'RUNNING'
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            logging.info('The custom labels model was already deployed')
        else:  # unexpected error
            raise e
    globals()['started_project_version'] = True


def stop_project_version() -> None:
    logging.info(f'Stopping the Custom Labels project version')
    response: dict = rekognition.stop_project_version(
        ProjectVersionArn=PROJECT_VERSION_ARN
    )
    logging.info(f'Got response {response} from rekognition')


def detect_labels(jpeg_image: io.BytesIO) -> Tuple[Label, float]:
    if not started_project_version:
        start_project_version()
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
