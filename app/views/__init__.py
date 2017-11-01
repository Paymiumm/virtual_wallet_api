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
from api_version.utils import validate_
from data import create_account_handler,resend_mail,update_account_handler,otp_generator,log_user_in,search_user,load_Chat,transfer_funds_with_email,transfer_funds_with_number,virtual_wallet_handler
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
param.add_argument('kpN', type=inputs.regex("^(\S+)([A-z]+)([0-9]+)([-_]*)$"), help='PayPin serves as a transaction authenticating key', required=True)

model = api.model('Personal', {
    'ad_d_r_eSS': fields.String(description='The address of the user'),
    'statE': fields.String(description='The state of the user'),
    'city': fields.String(description='the city of the user'),
    'postalC': fields.String(description="postal code of the user's location"),
    'dob': fields.String(description='date of birth of the user'),
    'kpN': fields.String(description='PayPin for the user [6 characters]')
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
			paypin=params.get('kpN')


			
			print "Updating personal details..."
			exec_account_update=update_account_handler(add=add,state=state,city=city,postal=postal,dob=dob)
			create_virtual_wallet=virtual_wallet_handler(paypin=paypin)
			print exec_account_update
			print create_virtual_wallet
			if exec_account_update==True and create_virtual_wallet==True:
				return json_response(res='true',reason="Personal Data was inserted into Table successfully")#if all went well

			if exec_account_update=='error' or create_virtual_wallet=='error':
				return json_response(res='error',reason="User was not found, or validation error")#if all went well

			else:
				#code exception occured
				return json_response(res='false',reason="An exception was thrown, either SQL error or user does not exist or invalid state was selected")
		else:
			return json_response(res="not_logged",reason="No session was found for user")



#----------------------------------------------------------------------------------
#	end of virtual wallet creation script and personal data updating script
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
		# print log_user_in(user=user,pwd=pwd,device=did)
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
		return search_user(query)
		# return json_response(res="hy")
		

#----------------------------------------------------------------------------------
#	end of search script
#----------------------------------------------------------------------------------



#----------------------------------------------------------------------------------
"""
	This handles recieve funds functionality for users, it also makes use of it's parser and marshal to ensure  
	proper passing of valid data
"""
#----------------------------------------------------------------------------------

param___ = api.parser()  # parsing arguments
param___.add_argument('type', type=inputs.regex("[A-z]{2,}"), help='Invalid reception of funds type', required=True)
param___.add_argument('amount', type=inputs.regex("(\d)"), help='Invalid Amount format', required=True)

model = api.model('Recieve_Funds', {
    'type': fields.String(description='Just use QRcode for now'),
    'amount': fields.Integer(description='Amount To Recieve...')
    
})

@api.expect(model, validate=True)
@api.doc(responses={
    201: 'Success',
    401: 'Validation Error',
    'Msg': 'The API is used to generate qr token (note: in v1, qrcode is the only supported mode of recieving funds)'
})
class recieve_funds_handler(Resource):


	"""
	This class handles the searching of user's from paymiumm, to start using the paymiumm magic functionality
	it takes one parameter which is query
	method:Get
	"""
	def post(self,query):
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
		


#----------------------------------------------------------------------------------
"""
	This handles the transfer of funds between users and non-users, it also makes use of it's parser and marshal to ensure  
	proper passing of valid data
"""
#----------------------------------------------------------------------------------
# transfer_param = api.parser()  # parsing arguments
# transfer_param.add_argument('type', type=inputs.regex("[A-z]{2,}"), help='Invalid Transaction Type', required=True)
# transfer_param.add_argument('amount', type=inputs.regex("\d+[.]?\d{2}"), help='Invalid Amount format', required=True)
# transfer_param.add_argument('data', type=str, help='Invalid Data format')

# model = api.model('Transfer_Funds', {
#     'type': fields.String(description='Transaction type.....either email/numb'),
#     'amount': fields.String(description='Amount To Send...'),
#     'data': fields.String(description='Data is best used to hold details of the transaction and can either be a phone number or email...'),
#     # 'email': fields.String(description='Email Of recipient...')
    
# })

# @api.expect(model, validate=True)
# @api.doc(responses={
#     201: 'Success',
#     401: 'Validation Error',
#     'Msg': 'The API is used to transfer funds between users and non users either tru the email system or phone network',
#     'Others': 'Always specify how you want funds to be transfered....if you choose email then email must be provided',
#     'Data': "Data is best used to hold details of the transaction and can either be a phone number or email..."
# })
# class transfer_funds_handler(Resource):
# 	"""
# 	This class handles the sending of fuuds among user's and non-user's of paymiumm, to start using the paymiumm magic functionality
# 	it takes three parameter which is query
# 	method:Post
# 	"""
# 	def post(self):
# 		params = transfer_param.parse_args()
# 		type_=params.get("type")
# 		data=params.get("data")
# 		amount=params.get("amount")

		
# 		if type_.lower()=="email" and validate_("email",data) == True:
# 			return transfer_funds_with_email(data=data,amount=amount)

# 		elif type_.lower()=="number" and validate_("reg_number",data) == True or validate_("number",data) == True:

# 			return transfer_funds_with_number(data=data,amount=amount)

# 		else:

# 			return json_response(res="shit ain't found")			





class testSession(Resource):
	"""docstring for testSession"""
	def get(self,name):
		session['user']=name
		session['device']=name
		return json_response(res="done")
		


#---------------------------------------------------------------------------------
#  script below handles sending of money through sms or email
#----------------------------------------------------------

transfer_email_param = api.parser()
transfer_email_param.add_argument('email',type=inputs.regex("([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+"), required=True, help='Should not be left blank')
transfer_email_param.add_argument('amount',type=inputs.regex("\d+[.]?\d{2}"), required=True, help='Should not be left blank')
transfer_email_param.add_argument('message', required=False, help='An optional value')

model = api.model('Transfer_Funds_Email', {
    'message': fields.String(description='optional message to accompany the funds transfer'),
    'amount': fields.String(description='Amount To Send...',required=True),
    'email': fields.String(description='Email of the user to recieve the funds...',required=True),
    # 'email': fields.String(description='Email Of recipient...')
    
})

@api.expect(model, validate=True)
@api.doc(responses={
    200: 'success',
    401: 'failed'
})
class send_transact_email(Resource):

	"""
	This class handles the sending of fuuds among user's and non-user's of paymiumm using email, to start using the paymiumm magic functionality
	it takes three parameter which is email,amount,message
	method:Post
	"""
	def post(self):
		params = transfer_email_param.parse_args()
		if 'user' in session and 'device' in session:
			email=params.get("email")
			msg=params.get("message")
			amount=params.get("amount")

			execute_action = transfer_funds_with_email(email=email, amount=amount, message=msg)

			if execute_action:
				return json_response(res='sent', reason='email was sent successfully')
			else:
				print (execute_action)
				return json_response(res='failed', reason='an error occurred while processing')

		else:

			return json_response(res='not_logged', reason='no user is loggged in')

transfer_text_param = api.parser()
# transfer_text_param.add_argument('number',type=inputs.regex("([0|\+[0-9]{1,5})?([7-9][0-9]{9})"), required=True, help='Should not be left blank')
# transfer_text_param.add_argument('amount',type=inputs.regex("\d+[.]?\d{2}"), required=True, help='Should not be left blank')
# transfer_text_param.add_argument('message', required=False, help='An optional value')

transfer_text_param.add_argument('number', type=inputs.regex("([0|\+[0-9]{1,5})?([0-9][0-9]{9})"), help='Number Should not be left blank', required=True)
transfer_text_param.add_argument('amount', type=inputs.regex("\d+[.]?\d{2}"), help='Invalid Amount format', required=True)
transfer_text_param.add_argument('message', type=str, help='An optional value',required=False)

model = api.model('Transfer_Funds_Sms', {
    'number': fields.String(description='Number of the user to recieve the funds...',required=True),
    'amount': fields.String(description='Amount To Send...',required=True),
	'message': fields.String(description='optional message to accompany the funds transfer')
})
@api.expect(model, validate=True)
@api.doc(responses={
    200: 'success',
    401: 'failed'
})
class send_transact_sms(Resource):

	"""
	This class handles the sending of fuuds among user's and non-user's of paymiumm using sms, to start using the paymiumm magic functionality
	it takes three parameter which is number,amount,message
	method:Post
	"""

	def post(self):
		params = transfer_text_param.parse_args()
		number=params.get("number")
		msg=params.get("message")
		amount=params.get("amount")

		if 'user' in session and 'device' in session:
		# 	pass

			execute_action = transfer_funds_with_number(number=number, amount=amount, message=msg)

			if execute_action:
				return json_response(res='sent', reason='text was sent successfully')

			elif not execute_action:
				return json_response(res='failed', reason='an error occured while processing')
		else:

			return json_response(res='not_logged', reason='no user is loggged in')
