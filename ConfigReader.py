import yaml
import os

class ConfigReader:
	
	def __init__(self, file):
		self.config = yaml.safe_load(open(file))
	
	def getProperty(self, name):
		nameList = name.split(".")
		currentConfig = self.config
		for part in nameList:
			currentConfig = currentConfig[part]
		return os.environ.get(name.replace(".", "_"), currentConfig)
