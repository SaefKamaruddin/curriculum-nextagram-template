import os
from flask import request
import requests


def send_after_signup(receiver_email):
    print('sending email')
    return requests.post(
        "https://api.mailgun.net/v3/" +
        os.environ.get("MAILGUN_DOMAIN")+"/messages",
        auth=("api", os.environ.get('MAILGUN_API')),
        data={"from": "Nextagram<mailgun@" + os.environ.get("MAILGUN_DOMAIN") + ">",
              "to": receiver_email,
              "subject": "Sign up",
              "text": "Thank you for sigining up to nextagram"
              })


def send_after_donating(receiver_email):
    print('sending email')
    return requests.post(
        "https://api.mailgun.net/v3/" +
        os.environ.get("MAILGUN_DOMAIN")+"/messages",
        auth=("api", os.environ.get('MAILGUN_API')),
        data={"from": "Nextagram<mailgun@" + os.environ.get("MAILGUN_DOMAIN") + ">",
              "to": receiver_email,
              "subject": "Donation",
              "text": "Thank you for your donation"
              })


def send_after_receiving_donation(receiver_email):
    print('sending email')
    return requests.post(
        "https://api.mailgun.net/v3/" +
        os.environ.get("MAILGUN_DOMAIN")+"/messages",
        auth=("api", os.environ.get('MAILGUN_API')),
        data={"from": "Nextagram<mailgun@" + os.environ.get("MAILGUN_DOMAIN") + ">",
              "to": receiver_email,
              "subject": "Donation",
              "text": "You have received a donation"
              })
