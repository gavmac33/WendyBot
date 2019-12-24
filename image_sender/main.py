from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import firebase_admin
from firebase_admin import firestore
import os, random

def env_vars(var):
    return os.environ.get(var, 'Specified environment variable is not set.')

# Define global constants using environment variables
ACCOUNT_SID = env_vars("ACCOUNT_SID")
AUTH_TOKEN = env_vars("AUTH_TOKEN")
WARRIOR_BOT_NUMBER = env_vars("WARRIOR_BOT_NUMBER")
WENDYS_NUMBER = env_vars("WENDYS_NUMBER")
IMAGES_DB_PATH = env_vars("IMAGES_DB_PATH")
SMS_CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)

# Create messaging and database objects
fire_app = firebase_admin.initialize_app()
DATABASE = firestore.client()


def send_image(event, context):
    images = [img.to_dict() for img in DATABASE.collection(IMAGES_DB_PATH).get()]
    image = random.choice(images)

    SMS_CLIENT.messages.create(
        to=WENDYS_NUMBER,
        from_=WARRIOR_BOT_NUMBER,
        media_url=image["image_url"],
        body="WendysWarriorsBot- " + image["description"]
    )