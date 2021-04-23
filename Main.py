#!/bin/python
""" This file runs the entire bot and connects the various elements of it."""
from core import sanya, config, MoodChatBot
from termcolor import colored


sanya.start(bot_token=config["!TELEGRAM!"]["bot_token"])
print(colored("Sanya ready!", "green"))
sanya.run_until_disconnected()
