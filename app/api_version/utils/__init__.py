# ~ util package that would hold common functionalities and tools that all versions of the api would use
# (@: Name): "mailMorth"

# (@:Description): "email Management, and automation api code"

# (@:Author): "inteliJence development team"

# under the license of Apache License 2.0 and intelijence Protective Rights please edit and use it with all the care you can give

# this

# import the user handlers
# --------------------------------------
# Import all modules and extentions
# --------------------------------------
from user import Users
from flask_mail import Message
from ext_declaration import mail
from flask import current_app, render_template
from security import generate_confirmation_token, resend_confirmation_token, generate_transact_url, confirm_transact_url
from models import User, TransactDetails
import socket
import re
from sqlalchemy.exc import IntegrityError
import datetime
import threading
from werkzeug.security import generate_password_hash, check_password_hash
from twilio.rest import Client
from passgen import passgen
from ext_declaration import db

# --------------------------------------
# END IMPORTATIONS
# --------------------------------------



# --------------------------------------
# Start Work
# --------------------------------------

# def generate_one_time_password():
#     """passgen modules used to generate one time password"""
#     value = passgen(length=6, case='both', digits=True, letters=True, punctuation=False)
#     return value
# from app.email import send_email
# end all import

user = Users()  # start user manager


def send_email(to, subject, template):
    msg = Message(subject, recipients=[to], html=template, sender=current_app.config['MAIL_DEFAULT_SENDER'])
    mail.send(msg)


states = ['ABIA',
          'ADAMAWA',
          'AKWA IBOM',
          'ANAMBRA',
          'BAUCHI',
          'BAYELSA',
          'BENUE',
          'BORNO',
          'CROSS RIVER',
          'DELTA',
          'EBONYI',
          'EDO',
          'EKITI',
          'ENUGU',
          'GOMBE',
          'IMO',
          'JIGAWA',
          'KADUNA',
          'KANO',
          'KATSINA',
          'KEBBI',
          'KOGI',
          'KWARA',
          'LAGOS',
          'NASSARAWA',
          'NIGER',
          'OGUN',
          'ONDO',
          'OSUN',
          'OYO',
          'PLATEAU',
          'RIVERS',
          'SOKOTO',
          'TARABA',
          'YOBE',
          'ZAMFARA',
          'State']


def validate_(type_, value):
    if type_ == "username":

        if re.match("(\S+)([A-z]+)([0-9]*)([-_]*)", value):
            print()
            re.match("(\S+)([A-z]+)([0-9]*)([-_]*)", value)
            return True
        else:
            print("username regex error")
            return False

    elif type_ == "password":
        if re.match("(\S+)", value):
            return True
        else:
            print("password regex error")
            return False

    elif type_ == "fullname":
        if re.match("([A-z]+) ([A-z]+)", value):
            return True
        else:
            print("name regex error")
            return False

    elif type_ == "number":
        if re.match("([+]+)([0-9]+)", value):
            return True
        else:
            print("number regex error")
            return False

    elif type_ == "address":
        if re.match("^([0-9]+)(\s*)(\S*)([a-zA-Z ]+)(\s*)(\S*)", value):
            return True
        else:
            print("address regex error")
            return False

    elif type_ == "city":
        if re.match("[A-z]{2,}", value):
            return True
        else:
            print("city regex error")
            return False

    elif type_ == "date":
        if re.match("(\d+) (\d+) \d{4}", value):
            return True
        else:
            print("date regex error")
            return False

    elif type_ == "postal":
        if re.match("\d{6}", value):
            return True
        else:
            print("postal regex error")
            return False

    elif type_ == "state":
        for x in states:
            if x == value and value != "State":
                return True

        print("opps states is not valid")
        return False

    elif type_ == "email":
        if re.match("([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+", value):
            return True
        else:
            print("email regex error")
            return False


def send_sms(to_number, body):
    """This function is to send_sms using twillio"""

    # generate OTP

    account_sid = current_app.config['TWILIO_ACCOUNT_SID']
    auth_token = current_app.config['TWILIO_AUTH_TOKEN']
    twilio_number = current_app.config['TWILIO_NUMBER']
    client = Client(account_sid, auth_token)
    client.api.messages.create(to_number, body, from_=twilio_number)


def generate_onetime_password():
    # return generate_password_hash(str(random.random()))[20:26]
    value = passgen(length=6, case='both', digits=True, letters=True, punctuation=False)
    return value


def remove_otp(user):
    user_ = User.query.filter_by(email=user).first()
    user_.password_hash = ""
    db.session.add(user_.password_hash)
    db.session.commit()
    print(user)


def activate_mail(email):
    try:
        token = generate_confirmation_token(email)
        html = render_template('activateMail.html', confirm_url='http://127.0.0.1:8000/account/confirMail/' + token,
                               email='http://127.0.0.1:8000/account/resendConfirmation?email=' + email)

        subject = 'Paymiumm: Confirm Your Account'

        send_email(email, subject, html)
        return True
    except Exception as e:
        print(e)
        return False

    except socket.gaierror as e:
        print(e)
        return False

def resend_activate_mail(email=""):
    try:
        token = resend_confirmation_token(email)
        html = render_template('activateMail.html', confirm_url='http://127.0.0.1:8000/account/confirMail/' + token,
                               email='http://127.0.0.1:8000/account/resendConfirmation?email=' + email)

        subject = 'Paymiumm: Confirm Your Account'

        send_email(email, subject, html)
    except Exception as e:
        print(e)
        return False

    except socket.gaierror as e:
        print(e)
        return False


def exec_(email):
    t = threading.Timer(3, remove_otp, args=[email])
    t.start()
    return True


def send_one_time_mail(user):
    gP = generate_onetime_password()
    print(user)

    html = render_template('one_password_mail.html', one_time_password=gP)

    subject = 'Paymiumm: Your one-time password'

    try:

        send_email(user, subject, html)

        return str(gP)

    except Exception as e:
        print(e)
        return False

    except socket.gaierror as e:
        print(e)
        return False


def send_link_with_email(email, amount, user_id, message=None):
    try:
        details = {'email': email, 'amount': amount, 'customer_id': user_id}

        token = generate_transact_url(details)

        html = render_template('send_money_link.html', confirm_url='' + token, email='')
        subject = message

        if message is None:
            subject = ''

            send_email(email, subject, html)

        else:
            send_email(email, subject, html)

        return True

    except Exception as e:
        print(e)
        return False

    except socket.gaierror as e:
        print(e)
        return False


def send_link_with_text(number, amount, user_id, message=None):
    try:
        details = {'number': number, 'amount': amount, 'customer_id': user_id}
        token = generate_transact_url(details)

        subject = 'your payment link\n {}'.format(token) # add your own customize msg here

        if message is None:

            send_sms(to_number=number, body=subject)

        else:
            subject = '{}\n,  {}'.format(message, token)
            send_sms(to_number=number, body=subject)

        return True

    except Exception as e:
        print(e)
        return False


def confirm_link(email):
    try:
        details = confirm_transact_url(email)
        print(details)

        return True

    except Exception as e:
        print(e)
        return False


def save_payment_details(reference_no):
    try:
        user = TransactDetails(reference_id=reference_no)

        db.session.add(user)
        db.session.commit()

        return True

    except IntegrityError:
        db.session.rollback()
        return False


def send_transaction_details(email, subject, html):
    try:
        send_email(user, subject, html)

    except Exception as e:
        return False



