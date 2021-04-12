#!/bon/python
# https://regexone.com/
# config
# database 1 only when it is expressly called
# database 2 always
# to add : chi é Eila, random(♪♬), la random music as audio at night,
import random
import time
import json
from telethon import TelegramClient, events

config = json.load(open('config.json'))
client = TelegramClient('anon', config["api_id"], config["api_hash"])

mood = 0  # in base ad hour

def defmood() -> int:
    hour = int(time.strftime('%H'))
    if 0 <= hour < config["sleep"]:
        return 0
    elif config["sleep"] <= hour < config["day"]:
        return 1
    elif config["day"] <= hour < config["night"]:
        return 2
    else:
        return 0

# main
@client.on(events.NewMessage())
async def callinmessage(event):
    _msgdbnt = json.load(open('db2.json'))  # Open msg database for no tag
    _other = json.load(open('db3.json'))  # other stuff
    _msg = event.raw_text.lower()
    _mood = defmood()
    for element in _msgdbnt:
        if element in _msg:
            if len(_msgdbnt[element]) == 1:
                _mood = 0
            await event.reply(_msgdbnt[element][_mood])
            return
    if (event.is_group and config["botname"] in _msg) or event.is_private:
        _msgdb = json.load(open('db1.json'))  # Open msg database
        for element in _msgdb:
            if element in _msg:
                if _mood==0 and element in _other["custommessages"]:
                    if len(_other["custommessages"][element]) == 1:
                        _mood = 0
                    await event.reply(_other["custommessages"][element][random.randrange(0, (len(_other["custommessages"][element])))])
                    return
                else:
                    if len(_msgdb[element]) == 1:
                        _mood = 0
                    await event.reply(_msgdb[element][_mood])
                    return
        if _mood == 1:
            await event.reply(_other["elsewhensleep"][random.randrange(0, (len(_other["elsewhensleep"])))])
        else:
            await event.reply(_other["else"][random.randrange(0, (len(_other["else"])))])

client.start()
client.run_until_disconnected()
