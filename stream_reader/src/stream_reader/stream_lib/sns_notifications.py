import boto3
import logging
import os
from enum import Enum, auto

sns = boto3.client('sns', region_name=os.environ['REGION'])
logging.debug(f"Created boto SNS client on region {os.environ['REGION']}")

TOPIC_ARN = os.environ['TOPIC_ARN']
logging.debug(f'Will publish to topic ARN: {TOPIC_ARN}')
CAM_LINK = 'https://zoo.sandiegozoo.org/cams/polar-cam'
SPOTTED_MESSAGE = f'A polar bear has been spotted! Check out the live cam: {CAM_LINK}'
SPOTTED_SUBJECT = 'Polar bear sighting!'
LEFT_MESSAGE = "The polar bear is no longer visible from the live cam. We'll let you know the next time one is visible."
LEFT_SUBJECT = 'Polar bear no longer visible'


class AnimalStatus(Enum):
    VISIBLE = auto()
    NOT_VISIBLE = auto()


def send_notification(animal_status: AnimalStatus) -> None:
    logging.info(f'Publishing SNS notification with status {animal_status}')
    sns.publish(
        TopicArn=TOPIC_ARN,
        Message=SPOTTED_MESSAGE if animal_status == AnimalStatus.VISIBLE else LEFT_MESSAGE,
        Subject=SPOTTED_SUBJECT if animal_status == AnimalStatus.VISIBLE else LEFT_SUBJECT
    )
