#!/bin/python

# add this in crontab at 0 0 * * * (python ...) or(./)
import sqlite3
from random import randrange
from utils import get_messages
from time import strftime
import telebot  # pip install pyTelegramBotAPI
from os import listdir

bot_token = "1794569431:AAEnC99GBFyWJZvkL78G_oNeUyAsPhsW67Q"
tb = telebot.TeleBot(bot_token)


def birtday():
    messages = get_messages("schedule_messages")
    for item in messages["date"]:
        if item in strftime("%m %d"):
            for i in id_list:
                tb.send_message(i, messages["date"][item])
            return True
        return False


sql = sqlite3.connect('database.db')
cur = sql.cursor()
cur.execute("SELECT * FROM chat WHERE active= 1")
list = cur.fetchall()
sql.close()
id_list = [int(item[0]) for item in list]

if birtday() is False:
    if randrange(0,5) == 3:
        print("si")
        audio = open(
            str("messages/audio/" + listdir("messages/audio")[randrange(0, len(listdir("messages/audio")))]),
            'rb')
        for i in id_list:
            tb.send_audio(chat_id, audio)
    else:
        print("no")
