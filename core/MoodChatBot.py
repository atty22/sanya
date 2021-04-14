""" In this file there are the main chat bot functions. """
from random import randrange
from core import sanya, events, config
from utils import mood, get_messages, mood_to_words


@sanya.on(events.NewMessage)
async def mood_chat_bot_handler(event):
    _mood = mood()
    if event.is_private or event.is_group and config["!DEFAULT!"]["bot_name"] in event.raw_text.lower():
        available_keys = ({**get_messages("normal", "mood_chat_bot"), **get_messages("groups_auto", "mood_chat_bot")}
                          if event.mentioned is False
                          else {**get_messages("normal", "mood_chat_bot"), **get_messages("reply"),
                                **get_messages("groups_auto", "mood_chat_bot")})
        time_key = get_messages("exceptions", "mood_chat_bot")["time"][mood_to_words(_mood)]
        for word in time_key:
            if word in event.raw_text.lower():
                await event.reply(time_key[word][randrange(0, len(time_key[word]))])
                return
        for word in available_keys:
            if word in event.raw_text.lower():
                if len(available_keys[word]) !=3:
                    _mood=0
                (await (event.reply(available_keys[word][_mood])) if available_keys[word][_mood] != "" else None)
                return
        if config["!DEFAULT!"]["bot_name"] in event.raw_text.lower().replace(" ", "") or event.is_private:
            await event.reply(time_key["other"][randrange(0, len(time_key["other"]))])
            return
    if event.is_group:
        available_keys = (get_messages("groups_auto", "mood_chat_bot") if event.mentioned is False
                          else
                          {**get_messages("normal", "mood_chat_bot"), **get_messages("reply", "mood_chat_bot"), **get_messages("groups_auto", "mood_chat_bot")})
        for word in available_keys:
            if word in event.raw_text.lower():
                if len(available_keys[word]) !=3:
                    _mood=0
                await event.reply(available_keys[word][_mood])

