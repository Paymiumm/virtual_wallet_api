#~ version one of the paymiumm(virtual wallet payment messanger) api which would hold all the functionalities of our version one
#(@: Name): "VWM"

#(@:Description): "A mobile payment messanger with the aid of a virtual wallet"

#(@:Author): "Paymiumm development team"

#under the license of Apache License 2.0 and intelijence Protective Rights please edit and use it with all the care you can give

#import blueprint class


from flask import Blueprint,request,url_for,current_app
from flask_restplus import  reqparse, fields, inputs
from views import create_Account,resend_activation_mail,testSession,personal_form,generate_password_token,login_handler,search_handler,chat_view_handler
from ext_declaration import api
from twilio.rest import Client

#end all import



#----------------------------------------------------------------------------------
#Create API
#----------------------------------------------------------------------------------
api_v1 = Blueprint('api_v1', __name__)#create a blueprint structure of the flask class
api.init_app(api_v1,version='1.0', validate=True, catch_all_404s=True,title="Paymiumm's API",
    description='A mobile payment messanger with the aid of a virtual wallet')#initialize the api class by passing the flask object to it

#----------------------------------------------------------------------------------
#End all API Configs
#----------------------------------------------------------------------------------


#----------------------------------------------------------------------------------
#	Configure and activate every every
#----------------------------------------------------------------------------------
# from start import json#it's imported here because of the BluePrint being declared



#----------------------------------------------------------------------------------
#	End of activation
#----------------------------------------------------------------------------------










#---------------------------------------------------------------------
#start routin pages here
#---------------------------------------------------------------------


api.add_resource(create_Account,"/signup/")
api.add_resource(resend_activation_mail,"/resendConfirmation/")
api.add_resource(testSession,"/test/<string:name>/")
api.add_resource(personal_form,"/personal/")
api.add_resource(generate_password_token,"/generatePasswordToken/")
api.add_resource(login_handler,"/login/")
api.add_resource(chat_view_handler,"/<string:user>/chat/")
api.add_resource(search_handler,"/search/<string:query>/")



# api.add_resource(authUser,"/auth/<string:app>/<string:Key>")
# api.add_resource(connectMail,"/startService/<string:app>/<string:clientKey>")
# api.add_resource(createAcct,"/createAcct/<string:app>/<string:clientKey>")
# api.add_resource(addEAcct,"/addMail/<string:app>/<string:clientKey>")
# api.add_resource(logAcct,"/logAcct/<string:app>/<string:clientKey>")
# api.add_resource(activateAcct,"/cAcct/<string:activationCode>/<string:uName>/")
# api.add_resource(load_image,"/load_image/cache/<string:Type>/<string:app>/<string:clientKey>/<string:imgName>")
# api.add_resource(getUAcct,"/getUser/<string:app>/<string:clientKey>/<string:user>/<string:resGroup>/")
# api.add_resource(createAcct,"/createAcctV/<string:app>/<string:clientKey>")
		
	
