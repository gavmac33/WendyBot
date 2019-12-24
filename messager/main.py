from twilio.rest import Client
import os
import base64

def env_vars(var):
    return os.environ.get(var, 'Specified environment variable is not set.')

# Define global constants using environment variables
ACCOUNT_SID = env_vars("ACCOUNT_SID")
AUTH_TOKEN = env_vars("AUTH_TOKEN")
WARRIOR_BOT_NUMBER = env_vars("WARRIOR_BOT_NUMBER")
WENDYS_NUMBER = env_vars("WENDYS_NUMBER")
SMS_CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)


def message(event, context):
    message = base64.b64decode(event['data']).decode('utf-8')


    SMS_CLIENT.messages.create(
        to=WENDYS_NUMBER,
        from_=WARRIOR_BOT_NUMBER,
        body="WendysWarriorsBot- " + message
    )

