from CivUrlHandler import CivUrlHandler
from Bots.TelegramBot import TelegramBot
from CivCloudCommandHandler import CivCloudCommandHandler
from CivWebhookReceiver import CivWebhookReceiver
from ConfigReader import ConfigReader
import logging
import _thread

config = ConfigReader("configuration.yml")

logLevel = int(config.getProperty("CivCloudBot.logLevel"))
BaseURL = config.getProperty("CivCloudBot.BaseURL")
WebHookIP = config.getProperty("CivCloudBot.WebHookReceiver.ip")
WebHookPort = config.getProperty("CivCloudBot.WebHookReceiver.port")
TelegramApiKey = config.getProperty("CivCloudBot.Bots.Telegram.ApiKey")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logLevel)

urlHandler = CivUrlHandler()

handler = CivCloudCommandHandler(urlHandler, BaseURL)
bot = TelegramBot(TelegramApiKey, handler)

botmap = {bot.getType(): bot}

receiver = CivWebhookReceiver(WebHookIP, WebHookPort, urlHandler, botmap)

_thread.start_new_thread(bot.run, ())

receiver.run()

