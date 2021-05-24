import json
import base64
import logging
import json
from json import JSONDecodeError
import binascii
import traceback

class CivUrlHandler:

		def getPathForNotification(self, bottype, userid):
			"""
			Generates a Path for the Notification defined by bottype and userid
			
			Parameters
			----------
			bottype : str
				The type of bot for this Notification (e.g. "Telegram", "Discord")
			userid : string
				The id for the chat (or similar) for the bot to use to send the message to the right chat.

			Returns
			-------
			Path (string)
				The Path for this Notification containing a base64 encoded json
			"""
			notification = [{"type": bottype, "userid" : userid}]
			jNotification = json.dumps(notification)
			return base64.urlsafe_b64encode(jNotification.encode('utf-8')).decode("utf-8")
			
		def getNotificationsForPath(self, path):
			"""
			Gets the Notifications for the given path
			
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
			try:
				decoded = base64.urlsafe_b64decode(path)
				return json.loads(decoded.decode("utf-8"))
			except JSONDecodeError as e:
				traceback.print_exc()
				logging.error(e.msg)
				return None
			except binascii.Error as e:
				traceback.print_exc()
				logging.error(str(e))
				return None
				