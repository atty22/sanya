""" This file is the heart of the entire bot. Here is contained the client (sanya) variable. """
from telethon import TelegramClient, events
import configparser


config = configparser.ConfigParser()
config.read("config.ini")


sanya = TelegramClient("default", int(config["!TELEGRAM!"]["api_id"]), config["!TELEGRAM!"]["api_hash"])