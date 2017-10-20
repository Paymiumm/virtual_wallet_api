from flask_restplus import Resource

#----------------------------------------------------------------------------------
#Handler for the API connection request
#----------------------------------------------------------------------------------

class start(Resource):
	"""Accepts authKey as Key and appName as app from the clientA and produce a clientKey
		which would serve as an identity for clientA and must be returned on every request
	"""
	def get(self,app,Key):
		# return {"request":"success"}
		# Auth(conn,app,Key)

		return {"mailMorth":{"Request":{"version":1.0,"type":"aplication/json"},"Response":{"clientKey":"209uedjwsd83oeawj","Auth":True,"status":200,"type":"aplication/json"}}}