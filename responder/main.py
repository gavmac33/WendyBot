from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import firebase_admin
from firebase_admin import firestore
import os, random


def env_vars(request):
    return os.environ.get(request, 'Specified environment variable is not set.')


# Read in environment variables
MESSAGES_DB_PATH = env_vars("MESSAGES_DB_PATH")


# Create messaging and database objects
app = Flask(__name__)
fire_app = firebase_admin.initialize_app()
DATABASE = firestore.client()

MESSAGE_REQUEST_TEXTS = {"m", "message"}

@app.route("/sms", methods=['GET', 'POST'])
def responder(useless_arg):
    phone_num, body = parseApiCall(request.values) # dict containing data about response

    if body.lower() in MESSAGE_REQUEST_TEXTS:
        response = get_message()
    else:
        response = get_instructions()

    # text person back
    text = MessagingResponse()  # prepare a response
    text.message("WendysWarriorsBot- " + response)
    return str(text)


def parseApiCall(data):
    phone_num = data.get('From')
    body = data.get('Body').strip()  # make lower and strip leading spaces
    return phone_num, body


def get_message():
    message_docs = DATABASE.collection(MESSAGES_DB_PATH).get()
    messages = [msg.to_dict() for msg in message_docs]
    message_info = random.choice(messages)

    return """
    \"%s\"
    -%s""" % (message_info["message"], message_info["author"])

def get_instructions():
    return """Type one of the following commands:
    • Message- get a supporting message from someone who loves you"""
