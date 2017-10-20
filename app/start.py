#----------------------------------------------------------------------------------
# Describe project
#----------------------------------------------------------------------------------

#(@: Name): "VWM"

#(@:Description): "A mobile payment messanger with the aid of a virtual wallet"

#(@:Author): "Paymiumm development team"

#under the license of Apache License 2.0 and Paymiumm Protective Rights please edit and use it with all the care you can give

#(@:VWM-Type): "Api (RestLess)"

#(@:Language): "Python"

#(@:Language Compiler): "python 2.9"

#(@:Framework): "Flask"

#(@:Required-Modules): "Flask_json, Base64, PassLib, Flask, Flask_restPlus, Flask SQL Alchemy, Flask_Mail, Flask_Socket, python 2.7, **more to come**"

#wow if you are done with the above
#and
#you get it
#you are on the right track
#boom!!!!!!!! now lets start the job

#import the flask framework and all it's modules like the flask_restplus and api's methods
#import all classes used in routing from the classes package/directory to access all api handlers

#----------------------------------------------------------------------------------
#	end Description
#----------------------------------------------------------------------------------

from api_version.v1 import api_v1#~ import version1 of the api methods
from ext_declaration import api, VWM, db, mail, json
from config import DevelopmentConfig
from sqlalchemy import create_engine,MetaData
from simplekv.db.sql import SQLAlchemyStore
from datetime import timedelta
from flask_kvsession import KVSessionExtension
# from security import password
# from db import alch,mysql#import connector for database
# from mail.mail import mail#import connector for mail server





VWM.config.from_object(DevelopmentConfig)
VWM.permanent_session_lifetime = timedelta(minutes=30)


#------------------------------------
#	End of Configs
#------------------------------------


#------------------------------------
#	Intialize of Extensions
#------------------------------------

db.init_app(VWM)
mail.init_app(VWM)
json.init_app(VWM)


@json.invalid_json_error
def invalid_json(e):
    return json_response(status_=400, description='Not a Json')

@json.error_handler
def error_handler(e):
    return json_response(status_=401, description='An error occured')
#------------------------------------
#	More Complex Intialization of Extensions
#------------------------------------


engine = create_engine(VWM.config['SQLALCHEMY_DATABASE_URI'])
metadata = MetaData(bind=engine)
session_store = SQLAlchemyStore(engine, metadata, 'kvsession_table')
metadata.create_all()
kvsession_extension = KVSessionExtension(session_store, VWM)


#----------------------------------------------------------------------------------
#	end initialize all required values
#----------------------------------------------------------------------------------






#------------------------------------------------------
#|||||||||||||||||||||||||||||||||||||||||||||||||||||
#routing blueprints starts now
VWM.register_blueprint(api_v1, url_prefix='/paymiumm/v1')

#end of blueprint route
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#----------------------------------------------------------

# @VWM.route("/start/<string:VWM>/<string:Key>")
# def loadPage():


#start server
if __name__ == '__main__':
	VWM.run(port=2030,debug=True)


