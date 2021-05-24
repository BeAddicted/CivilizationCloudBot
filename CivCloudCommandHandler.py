
class CivCloudCommandHandler:
	"""
	Responsible for Handling commands from Bots. All Bots will share the same commands to initiate and modify its notifications.
	For each command there will be a function here that handles the command and returns a response text.
	
	Attributes
	----------
	Will be set by the constructor and should not be tampered with from the outside.
	
	urlHandler : CivUrlHandler
		The MongoClient to use for Database access.
	baseUrl : string
		The baseUrl to use when generating the Webhook URL.
	"""
	def __init__(self, urlHandler, baseUrl):
		self.urlHandler = urlHandler
		self.baseUrl = baseUrl

	def start(self, bottype, userid):
		"""
		Generate the URL for given bot and userid and return a message for the bot to send.
		"""		
		path = self.urlHandler.getPathForNotification(bottype, userid)
		
		return ("Hi,\n"
				"I'm the Civilization Play by Cloud Notifications Bot.\n"
				"I will notify you when it's your turn.\n\n"
				"To set me up open up your Civilization 6 Game Options. There you can set the Play by Cloud Webhook URL.\n"
				"Use the following URL: " + self.baseUrl + "/" + path +"\n\n"
				"*Attention* you need to set this up before starting the Play by Cloud Game.\n"
				"If you are already in a Play by Cloud Game and you want to start using Webhooks you can save the game and load it as new Play by Cloud Game.")
