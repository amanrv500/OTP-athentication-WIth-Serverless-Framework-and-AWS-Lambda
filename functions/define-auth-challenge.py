from typing import List

MAX_ATTEMPTS = 3

def lambda_handler(event, context):
    attempts = len(event['request']['session'])
    last_attempt = event['request']['session'][-1] if attempts > 0 else None

    if event['request']['session'] and any(attempt['challengeName'] != 'CUSTOM_CHALLENGE' for attempt in event['request']['session']):
        # Should never happen, but in case we get anything other
        # than a custom challenge, then something's wrong and we
        # should abort
        event['response']['issueTokens'] = False
        event['response']['failAuthentication'] = True
    elif attempts >= MAX_ATTEMPTS and last_attempt and last_attempt['challengeResult'] is False:
        # The user has given too many wrong answers in a row
        event['response']['issueTokens'] = False
        event['response']['failAuthentication'] = True
    elif attempts >= 1 and last_attempt and last_attempt['challengeName'] == 'CUSTOM_CHALLENGE' and last_attempt['challengeResult'] is True:
        # Right answer
        event['response']['issueTokens'] = True
        event['response']['failAuthentication'] = False
    else:
        # Wrong answer, try again
        event['response']['issueTokens'] = False
        event['response']['failAuthentication'] = False
        event['response']['challengeName'] = 'CUSTOM_CHALLENGE'

    return event





# import json

# def lambda_handler(event, context):    
#     try:
#         # If user is not registered
#         if event['request']['userNotFound']:
#             event['response']['failAuthentication'] = True
#             event['response']['issueTokens'] = False
#             raise Exception('User does not exist')

#         # Wrong otp even after 3 session
#         if event['request']['session'] and len(event['request']['session']) >= 3 \
#                 and not event['request']['session'][-1]['challengeResult']:
#             event['response']['failAuthentication'] = True
#             event['response']['issueTokens'] = False
#             raise Exception('Invalid OTP')

#         elif event['request']['session'] and len(event['request']['session']) > 0 \
#                 and event['request']['session'][-1]['challengeResult']:
#             event['response']['failAuthentication'] = False
#             event['response']['issueTokens'] = True
#             # The user provided the right answer; succeed auth
#             print('Correct OTP!')

#         else:
#             event['response']['challengeName'] = 'CUSTOM_CHALLENGE'
#             event['response']['failAuthentication'] = False
#             event['response']['issueTokens'] = False
#             # The user did not provide a correct answer yet; present challenge
#             print('not yet received correct OTP')

#     except Exception as error:
#         return error

#     return json.loads(json.dumps(event, default=str))

