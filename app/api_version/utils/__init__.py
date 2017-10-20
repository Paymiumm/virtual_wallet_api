#~ util package that would hold common functionalities and tools that all versions of the api would use
#(@: Name): "mailMorth"

#(@:Description): "email Management, and automation api code"

#(@:Author): "inteliJence development team"

#under the license of Apache License 2.0 and intelijence Protective Rights please edit and use it with all the care you can give

#this 

#import the user handlers
#--------------------------------------
# Import all modules and extentions
#--------------------------------------
from user import Users
from security import generateKey
from flask import session,request,current_app
from connect import loginMail
from flask_mail import Message
from ext_declaration import mail
from flask import current_app, render_template
from security import generate_confirmation_token, confirm_token,generate_recovery_token,confirm_recovery_token,\
    resend_confirmation_token, confirm_resend_confirmation_token
from models import User
import random
import socket
import re
import datetime
import threading
from werkzeug.security import generate_password_hash, check_password_hash
from twilio.rest import Client
from passgen import passgen
#--------------------------------------
# END IMPORTATIONS
#--------------------------------------



#--------------------------------------
# Start Work
#--------------------------------------

# def generate_one_time_password():
#     """passgen modules used to generate one time password"""
#     value = passgen(length=6, case='both', digits=True, letters=True, punctuation=False)
#     return value
# from app.email import send_email
#end all import

user=Users(__name__)# start user manager




def send_email(to, subject, template):
    msg = Message(subject,recipients=[to],html=template,sender=current_app.config['MAIL_DEFAULT_SENDER'])
    mail.send(msg)

states=['ABIA',
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


def validate_(type,value):
    if type=="username":

        if re.match("(\S+)([A-z]+)([0-9]*)([-_]*)",value):
            print re.match("(\S+)([A-z]+)([0-9]*)([-_]*)",value)
            return True
        else:
            print "username regex error"
            return False

    elif type=="password":
        if re.match("(\S+)",value):
            return True
        else:
            print "password regex error"
            return False

    elif type=="fullname":
        if re.match("([A-z]+) ([A-z]+)",value):
            return True
        else:
            print "name regex error"
            return False

    elif type=="number":
        if re.match("([+]+)([0-9]+)",value):
            return True
        else:
            print "number regex error"
            return False

    elif type=="address":
        if re.match("^([0-9]+)(\s*)(\S*)([a-zA-Z ]+)(\s*)(\S*)",value):
            return True
        else:
            print "address regex error"
            return False

    elif type=="city":
        if re.match("[A-z]{2,}",value):
            return True
        else:
            print "city regex error"
            return False

    elif type=="date":
        if re.match("(\d+) (\d+) \d{4}",value):
            return True
        else:
            print "date regex error"
            return False

    elif type=="postal":
        if re.match("\d{6}",value):
            return True
        else:
            print "postal regex error"
            return False


    elif type=="state":
        for x in states:
            if x==value and value!="State":
                return True

        print "opps states is not valid"
        return False

    elif type=="email":
        if re.match("([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+",value):
            return True
        else:
            print "email regex error"
            return False

def send_sms(to_number):
    """This function is to send_sms using twillio"""

    #generate OTP
    gP=generateOneTimePassword()
    otp = 'Your Paymiumm Login OTP is: {}'.format(gP)

    account_sid = current_app.config['TWILIO_ACCOUNT_SID']
    auth_token = current_app.config['TWILIO_AUTH_TOKEN']
    twilio_number = current_app.config['TWILIO_NUMBER']
    client = Client(account_sid, auth_token)
    client.api.messages.create(to_number, from_=twilio_number, body=body)



def generateOneTimePassword():
    
    # return generate_password_hash(str(random.random()))[20:26]
	value = passgen(length=6, case='both', digits=True, letters=True, punctuation=False)
	return value
 
def removeOTP(user):
    user_ = User.query.filter_by(email=user).first()
    user_.password_hash=""
    db.session.commit()
    print user

def  activateMail(email):
        try:
            token = generate_confirmation_token(email)
            html = render_template('activateMail.html', confirm_url='http://127.0.0.1:8000/account/confirMail/'+token,email='http://127.0.0.1:8000/account/resendConfirmation?email='+email)

            subject = 'Paymiumm: Confirm Your Account'

            send_email(email, subject, html)
            return True        
        except Exception,e:
            print e
            return False

        except socket.gaierror,e:
            print e
            return False


def  resend_activateMail(email=""):

        try:
            token = resend_confirmation_token(email)
            html = render_template('activateMail.html', confirm_url='http://127.0.0.1:8000/account/confirMail/'+token,email='http://127.0.0.1:8000/account/resendConfirmation?email='+email)

            subject = 'Paymiumm: Confirm Your Account'

            send_email(email, subject, html)
        except Exception,e:
            print e
            return False

        except socket.gaierror,e:
            print e
            return False


def exec_(email):
    t=threading.Timer(3,removeOTP,args=[email])
    t.start()
    return True


def sendOneTimeMail(user):

        gP=generateOneTimePassword()
        print user

        html = render_template('one_password_mail.html', one_time_password=gP)

        subject = 'Paymiumm: Your one-time password'

        try:

            send_email(user, subject, html)

            return str(gP)

        except Exception,e:
            print e
            return False

        except socket.gaierror,e:
            print e
            return False


def sendOneTimeText(number):
        try:
            gP=generateOneTimePassword()
            message = twilio_client.messages.create(to=number, from_="+2348114291038", body="Your Paymiumm OTP is "+gP)
            return True

        except Exception,e:
            print e
            return False

        except socket.gaierror,e:
            print e
            return False