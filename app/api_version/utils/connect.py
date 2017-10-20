import imaplib
import threading

#----------------------------------------------------------------------------------
"""Create a thread to handle the logging in of a user into an email system
"""
#----------------------------------------------------------------------------------

def connectToMailSystem(email,eClient,password,u,iD):
	try:
		from mail import ImapServer
		from mail.activateMail import sendActivationMail
		"""connect to email service"""
		# print email+" "+password+" "+eClient
		if eClient=="gmail.com":
			res=ImapServer()
			print "gmail was selected"
			rs=res.Imap5(T="g",user=email,p=password)
			print rs
			if rs[0]=='OK':
				print "loggedIn Successfully"
				return sendActivationMail(iD,email,u)
				# user.addMail(email,password,user)
			elif rs=="invalid":
				return "Invalid Crendentials"

		elif eClient=="yahoomail.com" or eClient=="yahoo.com" or eClient=="mail.yahoo.com" or eClient=="mail.yahoo.co.uk":
			res=ImapServer()
			print "yahoo was selected"
			rs=res.Imap5(T="y",user=email,p=password)
			print rs
			if rs[0]=='OK':
				print "loggedIn Successfully"
				return sendActivationMail(iD,email,u)
				# user.addMail(email,password,user)
				
			elif rs=="invalid":
				return "Invalid Crendentials"

		elif eClient=="hotmail.com":
			res=ImapServer()
			print "hotmail was selected"
			rs=res.Imap5(T="h",user=email,p=password)
			print rs
			if rs[0]=='OK':
				print "loggedIn Successfully"
				return sendActivationMail(iD,email,u)
				# user.addMail(email,password,user)
			elif rs=="invalid":
				return "Invalid Crendentials"

		elif eClient=="outlook.com":
			res=ImapServer()
			rs=res.Imap5(T="h",user=email,p=password)
			print rs
			if rs[0]=='OK':
				print "loggedIn Successfully"
				return sendActivationMail(iD,email,u)
				# user.addMail(email,password,user)
			elif rs=="invalid":
				return "Invalid Crendentials"
		else:
			res=ImapServer()
			rs=res.Imap5(T="o",user=email,p=password)
			print rs
			if rs[0]=='OK':
				print "loggedIn Successfully"
				return sendActivationMail(iD,email,u)
				# user.addMail(email,password,user)
			elif rs=="invalid":
				return "Invalid Crendentials"
				
	except  imaplib.IMAP4.error,e:
		print "Exception Error: "+str(e)
		print "Opps login error occured"
		print "Could not login to email client successfully"
		return False
		# return False

def loginMail(email,password,user):
	#~ user is a class and it is added here for the purpose of one of it's functionalities that would be used here
	try:
		if 1 < len(email.split("@")) :#~split to extract email clients name
			eClient=email.split("@")[1]
			t = threading.Thread(target=connectToMailSystem,args=(email,eClient,password,user))#~start a thread aND tryto login to the email system
			t.start()
			return [True,"",None]
		else:
			return [False,"","Opps invalid email strokes"]
	except Exception as e:
		print "Exception occured: "
		print e
		return [False,"","An Error Occured"]
		# raise e


