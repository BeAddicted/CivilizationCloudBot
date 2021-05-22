# CivilizationCloudBot
This is Webhook application for Civilization 6 Play By Cloud Games. It handles Webhooks from Civ and notifies the Player on his turn on a specified application.  
*Currently only Telegram is supported but more (like Discord) could be added.*  

It is written in Python and uses a MongoDB for persistence.

## Deployment

To use this you first need to create a Telegram Bot.  
Follow the offical instructions here: https://core.telegram.org/bots#3-how-do-i-create-a-bot


There are then two ways to deploy this application

### Native

To run this native you need to install Python 3.x  
Then install dependencies with `pip install pyyaml python-telegram-bot pymongo`  
You also need a MonogoDB instance running.  
See the configuration.yml to configure the application. There you need to set the Telegram API Key and your BaseURL.  
Start the Application with `python start.py`

### Docker
For easier deployment use the Docker deployment. Ready to use Docker and docker-compose files are included in this repo.  
The docker-compose will also set up a MongoDB instance and configure the Application to use it.  
Open the docker-compose.yml (or docker-compose-arm.yml for arm devices e.g. Raspberry Pi).  
Set your Telegram API Key and BaseURL  
Use `docker-compose build` to build the CivCloudBot image.  
Start the application with `docker-compose up -d`  

## Usage

The actual usage of the Bot is pretty easy. Each Player playing Play by Cloud Games can search the configured bot in Telegram and message `/start` to it.  
They will then receive their personal Play by Cloud Webhook URL and instructions on how set it up.

## Advanced Usage

The Bot supports more than one chat command and more could follow with more functionality.  
Those commands are:  
`/stop` to stop it from sending notifications.  
`/info` to send the related Webhook URL again.  
`/help` to display a help text with all commands.  
