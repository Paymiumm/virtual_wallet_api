#~ version one of the paymiumm(virtual wallet payment messanger) api which would hold all the functionalities of our version one
#(@: Name): "VWM"

#(@:Description): "A mobile payment messanger with the aid of a virtual wallet"

#(@:Author): "Paymiumm development team"

#under the license of Apache License 2.0 and intelijence Protective Rights please edit and use it with all the care you can give

#import blueprint class

from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_json import FlaskJSON
from flask import Flask


#end of importation


#----------------------------------------------------------------------------------
#Call the classes and all resources to be used for the functioning of the api
#----------------------------------------------------------------------------------
VWM=Flask(__name__)
db = SQLAlchemy()
mail = Mail()
json = FlaskJSON()
api=Api()
# session_store = RedisStore(redis.StrictRedis(host='127.0.0.1'))



#-----------------------------------------
#	Configurations of all data's is done here
#------------------------------------------
