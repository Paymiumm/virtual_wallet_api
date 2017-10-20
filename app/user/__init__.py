#session manager would be used to handle users 
#create store clientKeys  i
# this is a user AuthKey saving tool
from flask import request
import datetime

class Users:
	"""Users class *artificial session management"""
	user={}
	emails={}
	def __init__(self, Engine):
		print "user manager has started"

	def add(self,key="",value=""): #~add key

		self.user[key]={"key":value,"ip":request.remote_addr,"start":datetime.datetime.now()}

	def get(self,user=""): #~get user
		return self.user[user]

	def addMail(self,user,password,imapClass):
		#add Mails into mailing list
		self.emails[user]={"imap":imapClass,"pass":password}	
		print self.emails	

	def checkIP(self,app,ip):
		
		if app in self.user:
			if self.user[app]["ip"]==ip:
				#print self.user[app]["ip"]
				return True
			else:
				return False
		else:
			return False

	def isActive(self,app,ip):
		if self.checkIP(app,ip)==True:
			return True
		else:
			return False

	def isAuth(self,app,key,ip):
		try:

			if self.checkIP(app,ip)==True and self.user[app]["key"]==key:
				return True
			else:
				print "Value is {} ".format(self.user[app]["key"])
				return False
		except Exception,e:
			return False
		
# reqList={}
# def timeHandler():
	
# def reqTimer(app,ip):
# 	reqList[app]=ip
# 	t = Timer(20 * 60, timeout,app,ip)