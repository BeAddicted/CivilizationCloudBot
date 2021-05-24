import telegram
from telegram.ext import CommandHandler
from telegram.ext import Updater


class TelegramBot:
	"""
	Bot for usage with Telegram. Defines chat commands and handles all communication with Telegram.
	Handling for specific commands is forwarded to the CivCloudCommandHandler.
	"""
	def __init__(self, token, handler):
		self.type = "Telegram"
		self.handler = handler
		self.updater = Updater(token=token, use_context=True)
		dispatcher = self.updater.dispatcher
		start_handler = CommandHandler('start', self.start)
		dispatcher.add_handler(start_handler)
		print("Telegram Bot started")
		print(self.updater.bot.get_me())
	
	def getType(self):
		"""
		Get the of this bot. Always returns "Telegram"
		"""
		return self.type
	
	def run(self):
		"""
		Starts the bot, by polling for messages.
		"""
		self.updater.start_polling()
		
	def notify(self, text, chat_id):
		"""
		Notify the chat defined by chat_id with given text.
		"""
		self.updater.bot.send_message(chat_id=chat_id, text = text)

	def start(self, update, context):
		context.bot.send_message(chat_id=update.effective_chat.id, text=self.handler.start(self.type, update.effective_chat.id))
	
	
