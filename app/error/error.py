def friendsAdds(dbConnector,myDetails,userToAdd,presntUsername):
	try:
		sql_Statement= """SELECT * FROM users_circles_ WHERE id_circles=%d AND User_wtin_to_Add='%s' AND hasAccepted=%d"""%(myDetails,userToAdd[0],0)#databse query for searching if users has already been added
		dbcursor=dbConnector.cursor()
		dbcursor.execute(sql_Statement)#excute
		rows=dbcursor.fetchall()
		exchngVals={"bulean":False,"isCirclesBack":False}
		if rows:
			# from notification import createNotification
			# createNotification(dbConnector,"Circled",userToAdd[0],"""<a class="rs" href="#"""+presntUsername+""" ">"""+presntUsername+"""</a> has circled you back """,myDetails)
			sqlState="""UPDATE users_circles_ SET hasAccepted=%d WHERE id_circles=%d AND User_wtin_to_Add='%s' AND hasAccepted=%d"""%(1,myDetails,userToAdd[0],0)
			dbcursor=dbConnector.cursor()
			dbcursor.execute(sqlState)#excute
			dbConnector.commit()
			exchngVals['bulean']=True
			exchngVals['isCirclesBack']=True
			return exchngVals
			#*389*9*iucnumber
		else:
			print "user to add value is",userToAdd[0]
			sqlStatement="""INSERT INTO  users_circles_ (circles_name,id_circles,User_wtin_to_Add,hasAccepted) VALUES('%s','%s',%d,%d)"""%(userToAdd[1],userToAdd[0],myDetails,0)
			dbcursor=dbConnector.cursor()
			dbcursor.execute(sqlStatement)#excute
			dbConnector.commit()
			print "Circled successfully"
			exchngVals['bulean']=True
			return exchngVals

	except Exception,e:
		dbConnector.rollback()
		print "Sorry user could not add friend successfully because an error occured and it is ",e
		return exchngVals


def friendsUnAdds(dbConnector,myDetails,userToUNAdd):
	try: 
		sql_Statement= """SELECT * FROM users_circles_ WHERE id_circles='%s' AND User_wtin_to_Add=%d AND hasAccepted=%d OR id_circles='%s' AND User_wtin_to_Add=%d AND hasAccepted=%d"""%(myDetails,userToUNAdd[0],1,userToUNAdd[0],myDetails,1)#databse query for updating if users has already circled
		dbcursor=dbConnector.cursor()
		dbcursor.execute(sql_Statement)#excute
		rows=dbcursor.fetchall()
		if rows:#check if both users have circled if yes and one wants to put our update database to make the one still left to b d person tht sent the circles request
			sqlState="""UPDATE users_circles_ SET User_wtin_to_Add=%d,id_circles='%s',hasAccepted=%d WHERE id_circles='%s' AND User_wtin_to_Add=%d AND hasAccepted=%d OR id_circles='%s' AND User_wtin_to_Add=%d AND hasAccepted=%d"""%(userToUNAdd[0],myDetails,0,myDetails,userToUNAdd[0],1,userToUNAdd[0],myDetails,1)#this db does alot of logic like finding who exactly i want to uncircle and uncircling him without affecting others 
			dbcursor.execute(sqlState)#excute
			dbConnector.commit()
			print "Updated and now the other user i was circled with now is made the initiator to of our friendship"
			return True
		# EMPLOYEE WHERE
		else:
				sqlStatement="""DELETE FROM  users_circles_ WHERE id_circles='%s' AND User_wtin_to_Add=%d"""%(userToUNAdd[0],myDetails)
				# hasAccepted) VALUES('%s','%s',%d,%d)
				dbcursor.execute(sqlStatement)#excute
				dbConnector.commit()
				print "unCircled successfully"
				return True

	except Exception,e:
		dbConnector.rollback()
		print "Sorry user could not be unCircled friend successfully because an error occured and it is ",e
		return False