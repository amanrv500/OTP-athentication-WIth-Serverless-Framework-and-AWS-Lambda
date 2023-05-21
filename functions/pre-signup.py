import json
def lambda_handler(event, context):
    event['response']['autoVerifyEmail'] = True
    event['response']['autoVerifyPhone'] = True
    event['response']['autoConfirmUser'] = True
    return event
