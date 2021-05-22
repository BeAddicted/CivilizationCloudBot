from CivMongoClient import CivMongoClient
from Bots.TelegramBot import TelegramBot
from CivCloudCommandHandler import CivCloudCommandHandler
from CivWebhookReceiver import CivWebhookReceiver
from ConfigReader import ConfigReader
import logging
import _thread

config = ConfigReader("configuration.yml")

logLevel = int(config.getProperty("CivCloudBot.logLevel"))
MongoDBHost = config.getProperty("CivCloudBot.MongoDB.host")
MongoDBPort = config.getProperty("CivCloudBot.MongoDB.port")
BaseURL = config.getProperty("CivCloudBot.BaseURL")
WebHookIP = config.getProperty("CivCloudBot.WebHookReceiver.ip")
WebHookPort = config.getProperty("CivCloudBot.WebHookReceiver.port")
TelegramApiKey = config.getProperty("CivCloudBot.Bots.Telegram.ApiKey")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logLevel)

client = CivMongoClient(MongoDBHost, MongoDBPort)

handler = CivCloudCommandHandler(client, BaseURL)
bot = TelegramBot(TelegramApiKey, handler)

botmap = {bot.getType(): bot}

receiver = CivWebhookReceiver(WebHookIP, WebHookPort, client, botmap)

_thread.start_new_thread(bot.run, ())

receiver.run()

