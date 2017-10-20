from flaskext.mysql import MySQL#import sql into project
from flask.ext.sqlalchemy import SQLAlchemy

mysql=MySQL()#call mysql class from the import flaskext.sql
alch=SQLAlchemy()
# def Connectors(app):
# 	"""Connectors class handles database connection,query,request using flaskext.mysql"""
# 	try:		
# 		#SnapIO
# 		#configure database
# 		app.config['MYSQL_DATABASE_HOST']='localhost'#configure database host
# 		app.config['MYSQL_DATABASE_DB']='IJM_api'#configure database name
# 		app.config['MYSQL_DATABASE_PASSWORD']=''#CONFIGURE PASSWORD
# 		app.config['MYSQL_DATABASE_USER']='root'
# 		mysql.init_app(app)#initialize mysql to values set in app.config
# 		conn=mysql.connect()#connection
# 		print "connected to db"
# 		return conn
# 	except Exception,e:
# 		print e
# 		print "Failed to connect to database"

def DB():
	try:
		connector=mysql.connect()
		# cursor=connector.cursor()
		return connector
	except Exception,e:
		print e
		print "Failed to connect to database"

			# if alch.session.query("1").from_statement("SELECT 1").all():
			#     print 'It works.'
			# else:
			#     print 'Something is broken.'