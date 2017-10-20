#~ version one of the paymiumm(virtual wallet payment messanger) api which would hold all the functionalities of our version one
#(@: Name): "VWM"

#(@:Description): "A mobile payment messanger with the aid of a virtual wallet"

#(@:Author): "Paymiumm development team"

#under the license of Apache License 2.0 and intelijence Protective Rights please edit and use it with all the care you can give

#import blueprint class
from flask import session
from flask_restplus import Resource
from ext_declaration import api,db
from flask_restplus import reqparse, fields, inputs
from data import create_account_handler,resend_Mail,update_account_handler,otp_generator,log_user_in,search_user,load_Chat
from flask_json import json_response
from flask import request,render_template,make_response,session






#----------------------------------------------------------------------------------
"""
	This handles creation of account, it also makes use of it's parser and marshal to ensure  
	proper passing of valid data
"""
#----------------------------------------------------------------------------------

post_params = api.parser()  # parsing arguments
post_params.add_argument('usr', type=inputs.regex("(\S+)([A-z]+)([0-9]*)([-_]*)"), help='Username should not be left blank and must be a string', required=True)
post_params.add_argument('name', type=inputs.regex("([A-z]+) ([A-z]+)"), help='fullname should not be left blank and must be a string', required=True)
post_params.add_argument('email', type=inputs.regex("([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+"), help='email should not be left blank or is invalid')
post_params.add_argument('phn', type=inputs.regex("([+]+)([0-9]+)"), help='phone number should not be left blank', required=True)

model = api.model('User', {
    'usr': fields.String(description='The username for registering the user'),
    'name': fields.String(description='The fullname for registering the user'),
    'email': fields.String(description='the email for registering the user'),
    'phn': fields.String(description='Phone number for registering the user')
})
@api.expect(model, validate=True)
@api.doc(responses={
    201: 'success',
    401: 'validation error',
    'msg': 'Post fields to db to create a new user'
})
class create_Account(Resource):

	"""
	This class handles the creation of an account for a user , to start using the paymiumm magic functionality
	it takes four parameters which are email, usr, name, and phn
	method:Post
	"""
		
	def post(self):
		
		user_ = post_params.parse_args()
		session['user']=user_.get('email')
		print user_.get('email')

		
		print "Creating account..."
		exec_account_creation=create_account_handler(email=user_.get('email'),user=user_.get('usr'),name=user_.get('name'),num=user_.get('phn'))

		if exec_account_creation==True:
			return json_response(res='true',reason="Data was inserted into db successfully")#if all went well

		elif exec_account_creation=="user":
			return json_response(res='user',reason="Username already exist")#if usernAme already exist

		elif exec_account_creation=="email":
			#if email already exist
			return json_response(res='email',reason="Email already exist")

		elif exec_account_creation=="number":
			#if phone number already exist
			return json_response(res='number',reason="Phone number already exist")

		elif exec_account_creation=="mail":
			#email couldn't send sucessfully
			return json_response(res='mailErr',reason="Account activation mail wasn't sent successfully")

		elif exec_account_creation=="error":
			#regex validation was not passed
			return json_response(res='error',reason="validation failed because a member of the json parameters didn't match regex validations")

		else:
			#code exception occured
			return json_response(res='false',reason="An exception was thrown, an error occured either code wise, data wise or implementation wise, usually sql errors")


		# return Authenticate(app,clientKey,email,password)
		# startService()

#----------------------------------------------------------------------------------
#	end of account creation script
#----------------------------------------------------------------------------------






#----------------------------------------------------------------------------------
"""
	This handles the resending of user's activation email, it also makes use of it's parser and marshal to ensure  
	proper passing of valid data
"""
#----------------------------------------------------------------------------------

resend_mail_params = api.parser()  # parsing arguments
resend_mail_params.add_argument('email', type=inputs.regex("([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+"), help='email should not be left blank or is invalid')

model = api.model('ResendMail', {
    'email': fields.String(description='the email for registering the user'),

})
@api.expect(model, validate=True)
@api.doc(responses={
    201: 'success',
    401: 'validation error',
    'msg': 'Resend Activation Mail Again (cases of user not getting the initial mail)'
})
class resend_activation_mail(Resource):

	"""
	This class handles the resending of activation mail to the user's passed email, using the smtp functionality
	it takes one parameters which are email
	method:Post
	"""
		
	def post(self):
		
		param = resend_mail_params.parse_args()
		email= param.get('email')
		print param.get('email')


		print "Resending Mail..."
		exec_mail_resending=resend_Mail(email=email)

		if exec_mail_resending==True:
			return json_response(res='sent',reason="Data was inserted into db successfully")#if all went well

		elif exec_mail_resending=="invalid":
			#email couldn't send sucessfully
			return json_response(res='invalid',reason="The email was tampered with and therefore did not exist in the database/ was used on an already confirmed account")

		elif exec_mail_resending=="mail":
			#email couldn't send sucessfully
			return json_response(res='mailErr',reason="Account activation mail wasn't sent successfully",ses=session['user'])

		else:
			#code exception occured
			return json_response(res='false',reason="An exception was thrown, an error occured either code wise, data wise or implementation wise, usually sql errors or user attempted to change the email during request to something that didnt match our records or regex checking")



#----------------------------------------------------------------------------------
#	end of resending email script
#----------------------------------------------------------------------------------




#----------------------------------------------------------------------------------
"""
	This handles insertion of user's personal data, it also makes use of it's parser and marshal to ensure  
	proper passing of valid data
"""
#----------------------------------------------------------------------------------

param = api.parser()  # parsing arguments
param.add_argument('ad_d_r_eSS', type=inputs.regex("^([0-9]+)(\s*)(\S*)([a-zA-Z ]+)(\s*)(\S*)"), help='Address should not be left blank and must look like a true address', required=True)
param.add_argument('statE', type=inputs.regex("[A-z]{2,}"), help='state should not be left blank and must be a string', required=True)
param.add_argument('city', type=inputs.regex("[A-z]{2,}"), help='city should not be left blank and must be a string')
param.add_argument('postalC', type=inputs.regex("\d{6}"), help='postalCode should not be left blank', required=True)
param.add_argument('dob', type=inputs.regex("(\d+) (\d+) \d{4}"), help='date of birth should not be left blank', required=True)

model = api.model('Personal', {
    'ad_d_r_eSS': fields.String(description='The address of the user'),
    'statE': fields.String(description='The state of the user'),
    'city': fields.String(description='the city of the user'),
    'postalC': fields.String(description="postal code of the user's location"),
    'dob': fields.String(description='date of birth of the user')
})
@api.expect(model, validate=True)
@api.doc(responses={
    201: 'success',
    401: 'validation error',
    'msg': 'Insertion of personal data '
})
class personal_form(Resource):

	"""
	This class handles the creation of an account for a user , to start using the paymiumm magic functionality
	it takes four parameters which are email, usr, name, and phn
	method:Post
	"""
		
	def post(self):
		if( 'user' in session):
			params = param.parse_args()
			add=params.get('ad_d_r_eSS')
			state=params.get('statE')
			city=params.get('city')
			postal=params.get('postalC')
			dob=params.get('dob')


			
			print "Updating personal details..."
			exec_account_update=update_account_handler(add=add,state=state,city=city,postal=postal,dob=dob)
			print exec_account_update
			if exec_account_update==True:
				return json_response(res='true',reason="Personal Data was inserted into Table successfully")#if all went well

			if exec_account_update=='not_logged':
				return json_response(res='not_logged',reason="User is currently not logged in..or session has expired")#if all went well

			else:
				#code exception occured
				return json_response(res='false',reason="An exception was thrown, either SQL error or user does not exist or invalid state was selected")
		else:
			return json_response(res="false",reason="No session was found for user")


		# return Authenticate(app,clientKey,email,password)
		# startService()

#----------------------------------------------------------------------------------
#	end of account creation script
#----------------------------------------------------------------------------------




#----------------------------------------------------------------------------------
"""
	This handles generating of user's password, it also makes use of it's parser and marshal to ensure  
	proper passing of valid data
"""
#----------------------------------------------------------------------------------

param_ = api.parser()  # parsing arguments
param_.add_argument('usr', type=inputs.regex("[A-z]{2,}"), help='Invalid username or email', required=True)
param_.add_argument('t_y_pE', type=inputs.regex("[A-z]{2,}"), help='Specify the way you want to recieve your OTP', required=True)

otp_model = api.model('OTP', {
    'usr': fields.String(description='The username of the intending user to login'),
    't_y_pE': fields.String(description='Specify the way you want to recieve your OTP'),
})
@api.expect(otp_model, validate=True)
@api.doc(responses={
    201: 'success',
    401: 'validation error',
    'Msg': 'The API is used to generate password token for the user to login'
})

class generate_password_token(Resource):
	"""
	This class handles the generating and sending of OTP to user's mail or phone number to login, to start using the paymiumm magic functionality
	it takes two parameters which are email/usr and type
	method:Post
	"""
	def post(self):
		params = param_.parse_args()
		user=params.get('usr')
		type_=params.get('t_y_pE')
		otp_handler=otp_generator(user=user,type_=type_)
		if otp_handler==True:
				return json_response(res='success',reason="OTP was sent successfully")#if all went well

		elif otp_handler=='unconfirmed':
				return json_response(res='unconfirmed',reason="This account email hasn't been successfully activated")#if all went well

		elif otp_handler=='invalid':
				return json_response(res='invalid',reason="This account username/email doesn't exist")#if all went well

		else:
				return json_response(res='error',reason="It's either email/text message couldn't be sent successfully or a code error occured")#if all went well
		


#----------------------------------------------------------------------------------
#	end of generate token for login script
#----------------------------------------------------------------------------------


#----------------------------------------------------------------------------------
"""
	This handles login of user, it also makes use of it's parser and marshal to ensure  
	proper passing of valid data
"""
#----------------------------------------------------------------------------------

param__ = api.parser()  # parsing arguments
param__.add_argument('usr', type=inputs.regex("[A-z]{2,}"), help='Invalid username or email', required=True)
param__.add_argument('pwd', type=inputs.regex("(\S+)"), help='Invalid OTP Format', required=True)
param__.add_argument('t__Ukn__r_z_A_R', type=inputs.regex("(\S+)"), help='Invalid Device Identity Format', required=True)

login = api.model('Login', {
    'usr': fields.String(description='The username of the intending user to login'),
    'pwd': fields.String(description='The OTP you recieved'),
    't__Ukn__r_z_A_R': fields.String(description='The Device identity')
    
})

@api.expect(login, validate=True)
@api.doc(responses={
    201: 'success',
    401: 'validation error',
    'Msg': 'The API is used to login user into his account'
})
class login_handler(Resource):


	"""
	This class handles the login of user into his account, to start using the paymiumm magic functionality
	it takes two parameters which are email/usr and password
	method:Post
	"""
	def post(self):
		params = param__.parse_args()
		user=params.get('usr')
		pwd=params.get('pwd')
		did=params.get('t__Ukn__r_z_A_R')#device id
		return log_user_in(user=user,pwd=pwd,device=did)
		# return json_response(res="hy")
		

#----------------------------------------------------------------------------------
#	end of login script
#----------------------------------------------------------------------------------




#----------------------------------------------------------------------------------
"""
	This handles searching for users, it also makes use of it's parser and marshal to ensure  
	proper passing of valid data
"""
#----------------------------------------------------------------------------------



# model = api.model('Search', {
#     'query': fields.String(description='Search Query'),
    
# })

# @api.expect(model, validate=True)
@api.doc(responses={
    201: 'success',
    401: 'validation error',
    'Msg': 'The API is used to search for users'
})
class search_handler(Resource):


	"""
	This class handles the searching of user's from paymiumm, to start using the paymiumm magic functionality
	it takes one parameter which is query
	method:Get
	"""
	def get(self,query):
		print query
		return search_user(query)
		# return json_response(res="hy")
		

#----------------------------------------------------------------------------------
#	end of search script
#----------------------------------------------------------------------------------



#----------------------------------------------------------------------------------
"""
	This handles loading of users chat, it also makes use of it's parser and marshal to ensure  
	proper passing of valid data
"""
#----------------------------------------------------------------------------------




@api.doc(responses={
    201: 'success',
    401: 'validation error',
    'Msg': 'The API is used to load users chat'
})
class chat_view_handler(Resource):


	"""
	This class handles the searching of user's from paymiumm, to start using the paymiumm magic functionality
	it takes one parameter which is query
	method:Get
	"""
	def get(self,user):

		return load_Chat(user)
		# return json_response(res="hy")
		

#----------------------------------------------------------------------------------
#	end of search script
#----------------------------------------------------------------------------------
		

class testSession(Resource):
	"""docstring for testSession"""
	def get(self,name):
		session['user']=name
		session['device']=name
		return json_response(res="done")
		


