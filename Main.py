""" This file runs the entire bot and connects the various elements of it. """
from core import sanya, config
from termcolor import colored
from core import MoodChatBot


sanya.start(bot_token=config["!TELEGRAM!"]["bot_token"])
print(colored("Sanya ready!", "green"))
sanya.run_until_disconnected()
