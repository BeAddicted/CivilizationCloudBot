from http.server import HTTPServer, BaseHTTPRequestHandler
import logging
import json
from json import JSONDecodeError
import builtins
import traceback

#Text Template for Notifications
NotificationText = "Hey! {name} it's your turn #{turn} in '{game}'"
class CivWebhookReceiver:
	"""
	Responsible for receiving Civilization 6 Webhooks and handling them.
	
	Not the strange DataModle Civilization 6 gives out:
	{
	"value1": "the name of your game",
	"value2": "the player's Steam name",
	"value3": "the turn number"
	}

	Attributes
	----------
	Will be set by the constructor and should not be tampered with from the outside.
	
	address : str
		Address to listen on. Empty string to listen on all addresses.
	port : int
		Port to listen on.
	civMonogClient: CivMongoClient
		The MongoClient to use for Database access.
	botMap:
		Map of all bots containing BotType as key and the actual BotObject as value.
	"""
	
	def __init__(self, address, port, civMongoClient, botMap):
		self.address = address
		self.port = port
		self.client = civMongoClient
		self.botMap = botMap

	def generate_Handler(self):
		"""
		Generate the Handler Class for incoming requests. 
		Must be done here to define client and botMap in this function, so the Class (and with it all created Objects created by the HTTPServer) has access to those.
		"""		
		client = self.client
		botMap = self.botMap
		
		class CivWebhookHandler(BaseHTTPRequestHandler):
			def do_POST(self):	
				
				#get content
				content_length = int(self.headers['Content-Length'])
				payloadraw = self.rfile.read(content_length)
				logging.debug("Path {path} was called with payload\n {payload}".format(path = self.path, payload = payloadraw.decode('utf-8')))
				
				try:	
					#parse json
					payload = json.loads(payloadraw)
					
					#Create text from received data. Note that the payload from civs webhook api is rather bad named.
					text =  NotificationText.format(name = payload["value2"], turn = payload["value3"], game = payload["value1"])
					
					#get notifications for called path
					notifications = client.getNotificationsForPath(self.path.replace("/",""))
					
					#send text to all bots defined by notifications.
					#Note most of the time there will only be one but there could be multiple if someone wants multiple channels to be called.
					if notifications:
						for notification in notifications:
							botMap[notification["type"]].notify(text, notification["userid"])
					else:
						logging.info("Nothing to notify for path {path}".format(path = self.path))

					
					self.send_response(200)
					self.end_headers()
				except JSONDecodeError as e:
					traceback.print_exc()
					logging.error(e.msg)
					self.send_response(400)
					self.end_headers()
				except KeyError as e:
					traceback.print_exc()
					logging.error(str(e))
					self.send_response(400)
					self.end_headers()
		return CivWebhookHandler
		
	def run(self):
		"""
		Start the Receiver and wait for incomming HTTP requests
		"""
		server_address = (self.address, self.port)
		httpd = HTTPServer(server_address, self.generate_Handler())
		print('serving')
		httpd.serve_forever()
