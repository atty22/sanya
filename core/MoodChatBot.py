""" In this file there are the main chat bot functions. """
from core import sanya, events, config
from os import listdir
from random import randrange
from utils import mood, get_messages, mood_to_words, database
from datetime import datetime


@sanya.on(events.NewMessage)
async def mood_chat_bot_handler(event):
    timestart = datetime.now()
    if "/randomsong" in event.raw_text.lower():
        await event.get_chat()
        await sanya.send_file(event.chat_id, str("messages/audio/" + listdir("messages/audio")[
            randrange(0, len(listdir("messages/audio")))]))
        return
    if "/toggle" in event.raw_text.lower():
        await event.get_chat()
        await event.reply(database(event.chat_id))
        return
    _mood = mood()
    if event.is_private or event.is_group and config["!DEFAULT!"]["bot_name"] in event.raw_text.lower():
        time_key = get_messages("exceptions", "mood_chat_bot")["time"][mood_to_words(_mood)]
        for word in time_key:
            if word in event.raw_text.lower():
                await event.reply(time_key[word][randrange(0, len(time_key[word]))])
                return
        available_keys = ({**get_messages("normal", "mood_chat_bot"),
                           **get_messages("groups_auto", "mood_chat_bot")} if event.mentioned is False else {
            **get_messages("normal", "mood_chat_bot"), **get_messages("reply"),
            **get_messages("groups_auto", "mood_chat_bot")})
        for word in available_keys:
            if word in event.raw_text.lower():
                if len(available_keys[word]) != 3:
                    _mood = 0
                (await (event.reply(available_keys[word][_mood])) if available_keys[word][_mood] != "" else None)
                return
        if "/ping" in event.raw_text.lower():
            await event.reply(str("pong in :" + str(datetime.now() - timestart)[10:] + "ns"))
            return
        if config["!DEFAULT!"]["bot_name"] in event.raw_text.lower().replace(" ", "") or event.is_private:
            await event.reply(time_key["other"][randrange(0, len(time_key["other"]))])
            return
    if event.is_group:
        available_keys = (get_messages("groups_auto", "mood_chat_bot") if event.mentioned is False
                          else
                          {**get_messages("normal", "mood_chat_bot"), **get_messages("reply", "mood_chat_bot"),
                           **get_messages("groups_auto", "mood_chat_bot")})
        for word in available_keys:
            if word in event.raw_text.lower():
                if len(available_keys[word]) != 3:
                    _mood = 0
                await event.reply(available_keys[word][_mood])
        if "ping" in event.raw_text.lower():
            await event.reply(str("pong in " + str(datetime.now() - timestart)[10:] + "ns"))
            return
