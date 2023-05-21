import json

def lambda_handler(event, context):
    
    expected_answer = event['request']['privateChallengeParameters']['answer']
    try:
        if event['request']['challengeAnswer'] == expected_answer:
            event['response']['answerCorrect'] = True
            print('valid', expected_answer)
        else:
            event['response']['answerCorrect'] = False
            # raise Exception('Invalid OTP')
            print('Invalid', expected_answer)
    except Exception as e:
        return e
    return event
