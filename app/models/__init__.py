from ext_declaration import db
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import datetime
from flask import current_app





class User(db.Model):
    """UserMixin, This provides default implementations for the methods that Flask-Login
   expects user objects to have."""

    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(60))
    username = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    phone_number = db.Column(db.String(15))
    password_hash = db.Column(db.String(100))
    email_confirmed = db.Column(db.Boolean, default=False)
    account_confirmed = db.Column(db.Boolean, default=False)
    img_path = db.Column(db.String(100))
    dev_identity = db.Column(db.String(100),nullable=True)
    # user = db.relationship('PrivateDetails', backref='users', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not in readable format')

    @password.setter
    def password(self, plaintext):
        self.password_hash = generate_password_hash(plaintext)

    def verify_password(self, plaintext):
        if check_password_hash(self.password_hash, plaintext):
            return True
        return False

    def encode_auth_token(self, user_id):
        # set up a payload with an expiration time
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            return jwt.encode(payload,
                              not current_app.config['SECRET_KEY'],
                              algorithm='HS256'
                              )
        # return an error in string format if an exception occurs
        except Exception as e:
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            #  try to decode the token using our SECRET variable
            payload = jwt.decode(token, current_app.config['SECRET_KEY'])
            is_blacklisted_token = BlackListToken.check_blacklist(auth_token=payload)
            if is_blacklisted_token:
                return 'Token blaclisted, Please log in again'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"

    def __repr__(self):
        """This method is used for debugging"""
        return 'User {}'.format(self.username)


class BlackListToken(db.Model):
    __tablename__ = 'blacklist_token'

    id  = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(120), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.utcnow()

    @staticmethod
    def check_blacklist(auth_token):
    # check whether auth token has been blacklisted
        res = BlackListToken.query.filter_by(token=auth_token)
        if res:
            return True
        else:
            return False
        
    def __repr__(self):
        return '<id: token {}'.format(self.token)


class PrivateDetails(db.Model):

    __tablename__ = 'PrivateDetails'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200))
    city = db.Column(db.String(160))
    state = db.Column(db.String(100))
    postal_code = db.Column(db.String(50))
    date_of_birth = db.Column(db.String(20))
    user_id = db.Column(db.String(255))
    # users_id = db.Column(db.Integer, db.ForeignKey('User.id'))

    def __repr__(self):
        return 'User {}'.format(self.address)


class User_Msgs(db.Model):

    __tablename__ = 'paymiumm_msgs_from_users'

    id = db.Column(db.Integer, primary_key=True)
    sndrs_id = db.Column(db.Integer)
    sndrs_name = db.Column(db.String(255))
    recvrs_id =  db.Column(db.Integer)
    recvrs_name = db.Column(db.String(255))
    s_or_r_Amnt = db.Column(db.BigInteger)
    msg_type = db.Column(db.String(255))
    trnsction_info = db.Column(db.String(255))
    shrt_msg = db.Column(db.String(100))
    is_Read = db.Column(db.Boolean,default=False)
    sent_time_Date = db.Column(db.DateTime(20))

    def __init__(self,sndrs_name=None, recvrs_name=None):
        if not sndrs_name:
            raise ValueError("Sender's name cannot be left empty")

        if not recvrs_name:
            raise ValueError("Reciever's name cannot be left empty")
        self.sndrs_name=sender
        self.recvrs_name=recvrs_name

    def __repr__(self):
        return 'User {}'.format(self.sndrs_name)
    