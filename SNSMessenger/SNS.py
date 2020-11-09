
import os
import boto3
#These will need top be changed based on user and session.
# Create an SNS client
#THESE WILL NO LONGER WORK. NEED TO GET CURRENT USERS CREDENTIALS
sns = boto3.client('sns',aws_access_key_id = 'ASIAR6RIBEXYIS3YJ6XW',aws_secret_access_key = 'l0Vo7AQd2NBzemzg9s37p8fHTQzv2FcsGAh8+yAq', aws_session_token='FwoGZXIvYXdzEE0aDEcfJXt3/KyWz54OriK+ARh+z5HuDkrIwrXdV7UCqlBbvLENp7MttotkWOf/DN9pN8CIilaK3juW4iaCs9RI+GQY2nDGj6zI7VCBiM5LnY/fBSxmhf3UUamcDO+vr4j7KKWfL0YD8IhJ91MXpZhVKZO0Dno667s2rAZLIPSSIfCcR3v9ERq0uAmIvmgZoGRUX1auvDHahfxlSVaEXay+52qneaGEm6OLO2H0awv1eufrBMLoNhRhsY22aZIqX84tiqIFWHLc86Syv7MmPvgoxJT8/AUyLSOXQEqKxhByHgKS7086pPeUOOJfT6dLkWlaLiVhbIl0RXSeo12SsmSx721/VA==' ,region_name='us-east-1')

# Publish a simple message to the specified SNS topic
response = sns.publish(
    TopicArn='arn:aws:sns:us-east-1:134301689328:ZooTestTopic',    
    Subject='TestingZoo',
    Message='Hello World!',    
)
#The topic will send a message to Justin currently. Others can be added. 

# Print out the response
print(response)