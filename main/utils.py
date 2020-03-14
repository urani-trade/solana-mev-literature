"""
Util methods to be used accross the app.
"""

import os
import json
import smtplib

from pathlib import Path  
from dotenv import load_dotenv
from django.core.mail import send_mail


def load_json(filepath):
    """
    Given a path to a JSON file, loads and return
    it as a dictionary.
    """
    try:
        with open(filepath, 'r') as file:
            return json.load(file)

    except IOError as e:
        print(f'Could not open {filepath}: {e}')


def send_email(subject, email, message):
    """
    Sends an email.

    Args:
        subject {str}: An email subject message.
        email {str}: An email destination.
        message {str}: An email message.
    """
    try:
        NQZ_EMAIL = extract_env_var()['NQZ_EMAIL']
        send_mail(subject, message, NQZ_EMAIL, [email], fail_silently=False)
    except (OSError, smtplib.SMTPException, KeyError) as e:
        print('Error sending email to {0}: {1}'.format(email, e))


def extract_env_var():
    """
    Load all env variables from .env file 
    into a dictionary.
    """
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

    data = {}

    data['PORT'] = os.getenv('PORT')
    data['DB_USER'] = os.getenv('DB_USER')
    data['DB_NAME'] = os.getenv('DB_NAME')
    data['DB_PASSWORD'] = os.getenv('DB_PASSWORD')
    data['DB_HOST'] = os.getenv('DB_HOST')
    data['DB_PORT'] = os.getenv('DB_PORT')
    data['SECRET_KEY'] = os.getenv('SECRET_KEY')
    data['SENDGRID_API_KEY'] = os.getenv('SENDGRID_API_KEY')
    data['ADMIN_EMAIL'] = os.getenv('ADMIN_EMAIL')
    data['NQZ_EMAIL'] = os.getenv('NQZ_EMAIL')
    data['EMAIL_HOST'] = os.getenv('EMAIL_HOST')
    data['EMAIL_PORT'] = os.getenv('EMAIL_PORT')
    data['EMAIL_HOST_USER'] = os.getenv('EMAIL_HOST_USER')
    data['ADMIN_EMAIL'] = os.getenv('ADMIN_EMAIL')
    data['S3_BUCKET'] = os.getenv('S3_BUCKET')


    return data
