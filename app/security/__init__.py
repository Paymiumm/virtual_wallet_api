from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
import hashlib
from werkzeug.security import generate_password_hash,check_password_hash
import base64
import datetime


def generateKey(ApiKey):
    millis = datetime.datetime.now()
    encodedKey = base64.b64encode(hashlib.sha1(bytes(ApiKey+str(millis))).digest())
    return encodedKey.split("=")[0].replace("/"," $$")


def generate_hash(p):
    return generate_password_hash(p)


def validate_hash(phash, p):
    return check_password_hash(phash ,p)


def password():
    return "intelijence.team"


def generate_confirmation_token(email):
    ts = Serializer(current_app.config['SECRET_KEY'])
    return ts.dumps(email, salt=current_app.config['SECURITY_EMAIL_SALT'])


def confirm_token(token, expiration=84600):
    ts = Serializer(current_app.config['SECRET_KEY'])
    return ts.loads(token, salt=current_app.config['SECURITY_EMAIL_SALT'], max_age=expiration)


def generate_recovery_token(email):
    ts = Serializer(current_app.config['SECRET_KEY'])
    return ts.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def confirm_recovery_token(token, expiration=3600):
    ts = Serializer(current_app.config['SECRET_KEY'])
    return ts.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)


def resend_confirmation_token(email):
    ts = Serializer(current_app.config['SECRET_KEY'])
    return ts.dumps(email, salt=current_app.config['RESEND_EMAIL_SALT'])


def confirm_resend_confirmation_token(token, expiration=84600):
    ts = Serializer(current_app.config['SECRET_KEY'])
    return ts.loads(token, salt=current_app.config['RESEND_EMAIL_SALT'], max_age=expiration)


def generate_transact_url(details):
    ts = Serializer(current_app.config['SECRET_KEY'])
    return ts.dumps(details, salt=current_app.config['SECURITY_ID'])


def confirm_transact_url(token, expiration=3600):
    ts = Serializer(current_app.config['SECRET_key'])
    return ts.loads(token, salt=current_app.config['SECURITY_ID'], max_age=expiration)
