import re
import boto3
import random
import string
import json

def lambda_handler(event, context):
    secret_login_code = None
    if not event['request']['session'] or not len(event['request']['session']):
        phone = event['request']['userAttributes']['phone_number']
        secret_login_code = "123456"
        # str(100000 + random.randint(0, 900000))
        # This is a new auth session
        # Generate a new secret login code and SMS or mail it to the user
        # sns = boto3.client('sns')
    
        # sns.publish(
        #     PhoneNumber=phone,
        #     Message='Your OTP is: ' + secret_login_code
        # ) 
    else:
        # re-use code generated in previous challenge
        previous_challenge = event['request']['session'][-1]
        secret_login_code = re.search(r'CODE-(\d*)', previous_challenge['challengeMetadata']).group(1)
    
    event['response']['publicChallengeParameters'] = {'phone': event['request']['userAttributes']['phone_number']}
    # Add the secret login code to the private challenge parameters
    # so it can be verified by the "Verify Auth Challenge Response"
    event['response']['privateChallengeParameters'] = {'answer': secret_login_code}
    # Add the secret login code to the session so it is available
    event['response']['challengeMetadata'] = f'CODE-{secret_login_code}'
    return event
