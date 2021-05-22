from pymongo import MongoClient
import uuid

class CivMongoClient:
	"""
	Manages the MongoDB. Contains functions to create and modify Paths and Notifications in the MongoDB
	
	The following DataModel is used by this Client for the MongoDB:
	
	{
		"path": string - The Path that has to be called for the Notifications to trigger
		"notifications": list(Notification) - The Notifications related to the path
	}
	
	Notification:
	{
		type: string - Type of bot for this Notification.
		userid: string - Id for this Notification used by the bot to call send to the right chat.
	}
	
	As can be seen each document in the mongoDB consists of a "path" and a list of notifications that are persisted there.
	The Path herby represents the HTTP Path that the CIV Webhook shall trigger to notify the related Notifications.
	Each Path here is intended for one player of the Civilization Cloud Games, to notify on multiple channels (even though mostly it will only be one).
	There can be multiple Notifications (also of different types) for one HTTP Path even though in the first step this is mostly a one to one relation.
	
	A Notification consists of a Type (e.g. "Telegram", "Discord") to determine which Bot is responsible for handling this
	and a userid that shall be given to the bot so that it can notify the right user.
	
	Note that not only each Path is unique but also each Notification. So that we don't have multiple Paths notifying the same player.

	Attributes
	----------
	Will be set by the constructor and should not be tampered with from the outside.
	
	client : MongoClient
		The MonogClient to use by this CivMongoClient
	db : MonogDB
		The DB to use by this CIVMongoClient		
	"""
	def __init__(self, host, port):
		self.client = MongoClient(host+":"+str(port))
		self.db = self.client.civ
	
	def createPathForNotification(self, bottype, userid):
		"""
		Creates a new Path for the Notification defined by the two parameters in the Database
		
		Parameters
		----------
		bottype : str
			The type of bot for this Notification (e.g. "Telegram", "Discord")
		userid : string
			The id for the chat (or similar) for the bot to use to send the message to the right chat.

		Returns
		-------
		Boolean
			Indicating if a new Path has been created. If false a new Path has not been created but the existing one is returned.
		Path (string)
			The Path created for this Notification/or existing Path if Notification already existed in case false is returned.
		"""
		#check if there is already a path for this notification.
		path = self.getPathForNotification(bottype, userid)
		if path != None:
			# False -> Notification already exists. Return Path.
			# Else create new Path.
			return False, path
		path = uuid.uuid4().hex
		url = { "path" : path, "notifications": [{"type": bottype, "userid" : userid}]}
		self.db.paths.insert_one(url)
		return True, path
	
	def getNotificationsForPath(self, path):
		"""
		Gets the Notifications related to the given path from the Database
		
		Parameters
		----------
		path : str
			The Path to get Notifications for.
			
		Returns
		-------
		List
			List of Notifications for given Path
		
		OR
		
		None
			If given Path does not exist in Database.
		"""
		path = self.db.paths.find_one({"path" : path})
		if path == None:
			return None
		return path["notifications"]
	
	def addNotificationForPath(self, path, bottype, userid):
		"""
		Adds a new Notification to the path specified to the Database
		
		Parameters
		----------
		path : str
			The Path to add a Notification to.
		bottype : str
			The type of bot for the Notification to add (e.g. "Telegram", "Discord")
		userid : string
			The id for the chat (or similar) for the bot to use to send the message to the right chat.

		Returns
		-------
		Boolean
			Indicating if adding was successful or not.
		"""
		#check if there is already a path for this notification.
		existingPath = self.getPathForNotification(bottype, userid)
		if existingPath != None:
			# False -> Notification already exists.
			return False
		result = self.db.paths.update_one({"path" : path}, {"$push": { "notifications": {"type": bottype, "userid" : userid}}})
		if result.modified_count == 1:		
			return True
		else:
			return False
	
	def removeNotification(self, bottype, userid):
		"""
		Removes a Notification from the Database. 
		If this results in a Path having no related Notifications anymore, the whole document is deleted.
		
		Parameters
		----------
		bottype : str
			The type of bot for the Notification to remove (e.g. "Telegram", "Discord")
		userid : string
			The id for the chat (or similar) of the Notification to remove

		Returns
		-------
		Boolean
			Indicating if removing was successful or not.
		"""
		#check path for the given Notification. If there is none the Notification to remove does not exist -> return False
		path = self.getPathForNotification(bottype, userid)
		if path == None:
			return False
		#After we got the path we check how many notifications are registered for the found path.
		#If only one delete the whole document
		notifications = self.getNotificationsForPath(path)
		if len(notifications) <= 1:
			self.db.paths.delete_one({"path": path})
			return True
		
		#If there are multiple update the document and remove only the given notification
		self.db.paths.update_one({"path": path}, {"$pull": { "notifications": {"type": bottype, "userid" : userid}}})
		return True
		
	
	def getPathForNotification(self, bottype, userid):
		"""
		Get the path for a Notification specified by the parameters form the Database.
		
		Parameters
		----------
		bottype : str
			The type of bot for the Notification to search (e.g. "Telegram", "Discord")
		userid : string
			The id for the chat (or similar) of the Notification to search

		Returns
		-------
		str
			Path related to the given Notification
		"""
		match = self.db.paths.find_one({ "notifications": {"$elemMatch" : {"type": bottype, "userid" : userid}}})
		if match == None:
			return None
		return match["path"]

