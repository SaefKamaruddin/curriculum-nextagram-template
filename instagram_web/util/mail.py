import os
from flask import request
import requests


def send_after_signup(receiver_email):
    print('sending email')
    return requests.post(
        "https://api.mailgun.net/v3/" +
        os.environ.get("MAILGUN_DOMAIN")+"/messages",
        auth=("api", os.environ.get('MAILGUN_API')),
        data={"from": "Padelle <mailgun@" + os.environ.get("MAILGUN_DOMAIN") + ">",
              "to": receiver_email,
              "subject": "Sign up",
              "text": "Sign up"
              })
