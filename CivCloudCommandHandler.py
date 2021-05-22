
class CivCloudCommandHandler:
	"""
	Responsible for Handling commands from Bots. All Bots will share the same commands to initiate and modify its notifications.
	For each command there will be a function here that handles the command and returns a response text.
	
	Attributes
	----------
	Will be set by the constructor and should not be tampered with from the outside.
	
	civMongoClient : civMongoClient
		The MongoClient to use for Database access.
	baseUrl : string
		The baseUrl to use when generating the Webhook URL.
	"""
	def __init__(self, civMongoClient, baseUrl):
		self.client = civMongoClient
		self.baseUrl = baseUrl

	def start(self, bottype, userid):
		"""
		Start the bot by generating a Webhook URL and give back instructions.
		If there is already a URL for this bot and user the existing URL ist given back with another text.
		"""		
		created, path = self.client.createPathForNotification(bottype, userid)
		
		if created:
			return ("Hi,\n"
					"I'm the Civilization Play by Cloud Notifications Bot.\n"
					"I will notify you when it's your turn.\n\n"
					"To set me up open up your Civilization 6 Game Options. There you can set the Play by Cloud Webhook URL.\n"
					"Use the following URL: " + self.baseUrl + "/" + path +"\n\n"
					"*Attention* you need to set this up before starting the Play by Cloud Game.\n"
					"If you are already in a Play by Cloud Game and you want to start using Webhooks you can save the game and load it as new Play by Cloud Game.")
		else:
			return ("Hi,\n"
					"I'm the Civilization Play by Cloud Notifications Bot.\n"
					"It seems like I already got a Webhook URL for you.\n"
					"To set me up open up your Civilization 6 Game Options. There you can set the Play by Cloud Webhook URL.\n\n"
					"Let me remind you of your URL: "+ self.baseUrl + "/" + path +"\n"
					"If you want to get a new one use \"/stop\" to stop me from sending you updates. Then you can use \"/start\" again to get a new URL.\n"
					"*Attention* you need to set this up before starting the Play by Cloud Game.\n"
					"If you are already in a Play by Cloud Game and you want to start using Webhooks you can save the game and load it as new Play by Cloud Game.")

	def stop(self, bottype, userid):
		"""
		Stop the bot by removing the Notification for this bot and user from the Database.
		"""	
		success = self.client.removeNotification(bottype, userid)
		if success:
			return ("I will stop sending you Notifications\n"
					"You can use \"/start\" again to get a new URL if you want to use me again.")
		else:
			return ("It seems like I don't have any Notification registered for you.\n"
					"There is nothing to stop for me")
	
	def info(self, bottype, userid):
		"""
		Get the current URL
		"""
		path = self.client.getPathForNotification(bottype, userid)
		if path != None:
			return ("You're current URL is "+ self.baseUrl + "/" + path +"\n"
					"To set me up open up your Civilization 6 Game Options. There you can set the Play by Cloud Webhook URL\n\n"
					"*Attention* you need to set this up before starting the Play by Cloud Game.\n"
					"If you are already in a Play by Cloud Game and you want to start using Webhooks you can save the game and load it as new Play by Cloud Game")
		else:
			return ("It seems like I don't have any URL for you yet\n"
					"Use \"/start\" to get instruction on how to set me up.")
	
	def help(self):
		return ("Hi,\n"
				"I'm the Civilization Play by Cloud Notifications Bot.\n"
				"You can use the following commands to talk to me:\n"
				"\"/start\" - to get a WeebhookURL and instruction on how to set me up\n"
				"\"/stop\" - to stop me from sending you updates here.\n"
				"\"/info\" - to let me send you your current Webhook URL again\n"
				"\"/help\" - to display this help text")
