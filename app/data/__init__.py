#general model package please use with care
#don't tamper if you can't hamper
#dnt touch what you cant fix
#::-api.paymiumm (model package)
from werkzeug.security import generate_password_hash,check_password_hash
from time import gmtime, strftime
from flask import session,make_response,jsonify
from security import generateHash,validateHash,generateKey
from api_version.utils import activateMail,validate_,resend_activateMail,sendOneTimeMail,send_sms,exec_
from ext_declaration import db
from models import User, PrivateDetails, BlackListToken,User_Msgs
from sqlalchemy.exc import IntegrityError
import datetime
from flask_json import json_response


#let the job begin


def create_account_handler(user="",email="",name="",num=""):
		"""
		This function would be used to insert data into db
		 and this function would handle the creation of account

		"""
		if validate_("username",user) and validate_("email",email) and validate_("fullname",name) and validate_("number",num):
            
			try:
				user_ = User.query.filter_by(username=user).first()
				email_ = User.query.filter_by(email=email).first()
				phn_ = User.query.filter_by(phone_number=num).first()

				if user_ is not None:

					print "username already exist"
                    # return make_response(jsonify({'res':'user'}))
					return "user"

				elif email_ is not None:

                    # return make_response(jsonify({'res':'email'}))
					return "email"

				elif phn_ is not None:

                    # return make_response(jsonify({'res':'number'}))
					return "number"

				else:
					user = User(full_name=name, email=email, username=user, phone_number=num, img_path="img_badge/fm0894tf9re.jpg")
					db.session.add(user)
					res=activateMail(email)
					if res!=False:
						db.session.commit()
                        # return make_response(jsonify({'res':'true'}))
						return True
					else:
						db.session.rollback()
                        # return make_response(jsonify({'res':'mailErr'}))
						return "mail"

			except IntegrityError,e:

				print "Exception @: \n"
				print e
				
				db.session.rollback()
                # return make_response(jsonify({'res':'false'}))
				return False
			except Exception,e:
                
				db.session.delete(user)
				db.session.commit()
				print "Error Occured: \n"+str(e)
                # return make_response(jsonify({'res':'false'}))
				return False
        
		else:
            # return make_response(jsonify({'res':'error'}))
			return "error"




def resend_Mail(email=""):
		"""
		This function would be used to resend activation link to user's mail

		"""
		if validate_("email",email):
            
			try:
				email_ = User.query.filter_by(email=email).first()

				if email_ is not None and not email_.account_confirmed:

					res=resend_activateMail(email)

					if res!=False:
                        # return make_response(jsonify({'res':'sent'}))
						return True
					else:
                        # return make_response(jsonify({'res':'mailErr'}))
						return "mail"

				else:
					# return make_response(jsonify({'res':'invalid'}))
					return "invalid"

			except IntegrityError,e:

				print "Exception: \n"
				print e
				
                # return make_response(jsonify({'res':'false'}))
				return False
			except Exception,e:
                
				print "Error Occured: \n"+str(e)
                # return make_response(jsonify({'res':'false'}))
				return False
        
		else:
            # return make_response(jsonify({'res':'false'}))
			return False


def update_account_handler(add="",state="",city="",postal="",dob=""):
	# print "hy"
		if 'user' in session:

			if validate_("address",add) and validate_("state",state) and validate_("city",city) and validate_("postal",postal) and validate_("date",dob):
	            
				try:
					# User.query.filter_by(username=user).first()
					user_ = User.query.filter_by(username=session['user']).first()
					# return make_response(jsonify({'res':str(session['user'])}))

					if user_ is not None:
						try:
							pDtails = PrivateDetails(address=add, city=city, state=state, postal_code=postal, date_of_birth=dob,user_id=str(session['user']))
							db.session.add(pDtails)
							user_.account_confirmed=True
							db.session.commit()
							# return make_response(jsonify({'res':'true'}))
							print True
							return True 
						except Exception,e:
							db.session.delete(pDtails)
							db.session.commit()
							# print "Error Occured: \n"+str(e)
							# return make_response(jsonify({'res':'false'}))
							print e
							return False


					else:                    
						print "user does not exist already exist"

						# return make_response(jsonify({'res':'error'}))
						return 'error'

				except IntegrityError,e:
					db.session.rollback()
					print e
					# return make_response(jsonify({'res':'false'}))
					return False
				except Exception,e:
					db.session.rollback()
					print e
	                # db.session.delete(pDtails)
	                # print "Error Occured: \n"+str(e)
	                # return make_response(jsonify({'res':'false'}))
					return False
	        
			else:
	            # return make_response(jsonify({'res':'error'}))
				print "Validation error"
				return 'error'

		else:
			# return make_response(jsonify({'res':'error'}))
			print "User does not exist error"
			return 'not_logged'



def otp_generator(user="",type_=""):

	if validate_("username",user) or validate_("email",user):


		user = User.query.filter((User.email==user) | (User.username==user)).first()
		if user is not None:
				if user.email_confirmed:
                        

						try:
							if type_=="email":
								res=sendOneTimeMail(user.email)
								if res!=False:                                        
                                    
									user.password_hash=res
									db.session.commit()
									# exec_(str(user.email))
									print "username password change is done"
                                    # return make_response(jsonify({'res':'success'}))
									return True

								else:
									print "error in connection so email could not be sent successfully"
									# print make_response(jsonify({'res':'error'}))
                                    # return make_response(jsonify({'res':'error'}))
									return False

							else:
								try:
									res=send_sms(user.phone_number)
									user.password_hash=res
									db.session.commit()
									exec_(str(user.email))
									print "username password change is done"
									return True
								except:

									print "error in connection so text could not be sent successfully"
									# print make_response(jsonify({'res':'error'}))
                                    # return make_response(jsonify({'res':'error'}))
									return False



						except Exception,e:

								print "error in occured"
								print e
                                # return make_response(jsonify({'res':'error'}))
								return False

				else:
                    # return make_response(jsonify({'res':'unconfirmed'}))
					print 'unconfirmed'
					return 'unconfirmed'

		else:
			# return make_response(jsonify({'res':'unconfirmed'})) 
			print 'invalid'
			return 'invalid'

	else:
		print "opps"
        # return make_response(jsonify({'res':"invalid"}))
		return 'invalid'



def log_user_in(user="",pwd="",device=""):
	if validate_("username",user) or validate_("email",user) and validate_("password",pwd):


		user = User.query.filter((User.email==user) | (User.username==user)).first()#check if user exist
		if user is not None and user.password_hash==pwd:
			if user.email_confirmed and user.account_confirmed:
				
				try:
					user.dev_identity=device
					user.password_hash=""
					db.session.commit()
					session['user']=user.username
					session['device']=user.dev_identity
					now = datetime.datetime.now()
					return make_response(jsonify({'res':'true','da_t_e':str(now.year),'userId':str(session['user']),'user':str(user.username),'t_k_n_t_R': user.dev_identity,'user_email':str(user.email),'user_img':str(user.img_path)}))

				except Exception,e:

					print "Error at:\n"
					print e
					db.session.rollback()
					return make_response(jsonify({'res':"error"}))
			elif  user.email_confirmed and not user.account_confirmed:
				try:
					user.dev_identity=device
					user.password_hash=""
					db.session.commit()
					session['user']=user.username
					session['device']=user.dev_identity
					now = datetime.datetime.now()
					return make_response(jsonify({'res':'accountUnconfirmed','da_t_e':str(now.year),'userId':str(session['user']),'user':str(user.username),'t_k_n_t_R':user.dev_identity,'user_email':str(user.email),'user_img':str(user.img_path)}))

				except Exception,e:

					print "Error at:\n"
					print e

					db.session.rollback()
					return make_response(jsonify({'res':"error"}))

			else:
				
				return make_response(jsonify({'res':"unconfirmed"}))

		else:
			print "false user name/email does not exist"
			return make_response(jsonify({'res':"false"}))


	else:
		print "false invalid format"
		return make_response(jsonify({'res':"false"}))
	



def search_user(query):
	if 'user' in session and 'device' in session:
		try:
			users=User.query.filter(User.username.like("%"+query+"%")).all()
			# print users
			if users:
				results=[]
	            # print user[0].img_path
				for user in users:

					if user.username==session['user']:
						print user
						print "naf this is the user that is already logged Into the system\n"   
					else:
						print "not logged user"
						print user
						results.append({"user":{"username":user.username,"img":user.img_path}})
						print results
				return make_response(jsonify({'res':results,'status':True}))
			else:
				print "no result found"
				return make_response(jsonify({'res':"false",'status':False}))
		except Exception,e:

			print e
			return make_response(jsonify({'res':"error",'status':False}))
	else:
		print "User not logged in"
		return make_response(jsonify({'res':"not_logged",'status':False}))


def load_Chat(user):
    try:
        if 'user' in session:
            # print user
            users=User_Msgs.query.filter((User_Msgs.sndrs_name==session['user']) & (User_Msgs.recvrs_name==user) | (User_Msgs.sndrs_name==user) & (User_Msgs.recvrs_name==session["user"])).all()
            if users:
                result=[]
                for user in users:
                    # print user.sndrs_name
                    #logic for determining sender and reciever goes in here
                    date=user.sent_time_Date
                    print str(date)
                    if user.sndrs_name.lower()==session['user'].lower():
                        print user.sndrs_name+" is the current user logged in"
                        #display this if this is the user currently loggedin
                        # formated_date=str(date).split(" ")[0]
                        result.append({'message':{'isUser':True,'transact_status':user.trnsction_info,'msg_type':user.msg_type,'shrt_msg':user.shrt_msg,'isSeen':user.is_Read,'amt':user.s_or_r_Amnt,'date':str(date)}})
                    else:

                        #update the message has already been marked as seen if false convert to true
                        print user.is_Read
                        if(user.is_Read==False):
                            user.is_Read=True
                            db.session.commit()
                            print "Messages has now been marked as read"
                        result.append({'message':{'isUser':False,'transact_status':user.trnsction_info,'msg_type':user.msg_type,'shrt_msg':user.shrt_msg,'isSeen':user.is_Read,'amt':user.s_or_r_Amnt,'date':str(date)}})
            else:
                print "Naf no result was found"
                return make_response(jsonify({'res':'no_msg'}))
     
            # print "user's chat to load is "+users.s_or_r_Amnt
            # return user
            
            # result.append({'message':{'isUser':True,'transact_status':'success','isSeen':True,'amt':100.00,'date':'2017-10-07 16:45:50'}})
            return make_response(jsonify({'res':result}))
        else:
			print "User not logged in"
			return make_response(jsonify({'res':"not_logged",'status':False}))
    except Exception,e:
        print e
        db.session.rollback()
        return make_response(jsonify({'res':'error'}))
    except IntegrityError:
        db.session.rollback()
