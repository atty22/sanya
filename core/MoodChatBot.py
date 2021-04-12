""" In this file there are the main chat bot functions. """
from random import randrange
from core import sanya, events, config
from utils import mood, get_messages, mood_to_words


@sanya.on(events.NewMessage)
async def mood_chat_bot_handler(event):
    if event.is_private or event.is_group and config["!DEFAULT!"]["bot_name"] in event.raw_text.lower():
        available_keys = ({**get_messages("normal", "mood_chat_bot"), **get_messages("groups_auto", "mood_chat_bot")}
                          if event.message.reply_to_msg_id is None
                          else {**get_messages("normal", "mood_chat_bot"), **get_messages("reply"),
                                **get_messages("groups_auto", "mood_chat_bot")})
        time_key = get_messages("exceptions", "mood_chat_bot")["time"][mood_to_words(mood())]
        for word in time_key:
            if word in event.raw_text.lower():
                await event.reply(time_key[word][randrange(0, len(time_key[word]))])
                return
        for word in available_keys:
            if word in event.raw_text.lower():
                (await (event.reply(available_keys[word][mood()])) if available_keys[word][mood()] != "" else None)
                return
        if config["!DEFAULT!"]["bot_name"] in event.raw_text.lower().replace(" ", ""):
            await event.reply(get_messages("exceptions", "mood_chat_bot")["onlysanya"]
                              [randrange(0, len(get_messages("exceptions", "mood_chat_bot")["onlysanya"]))])
            return
    if event.is_group:
        available_keys = (get_messages("groups_auto", "mood_chat_bot") if event.message.reply_to_msg_id is None
                          else
                          {**get_messages("reply", "mood_chat_bot"), **get_messages("groups_auto", "mood_chat_bot")})
        for word in available_keys:
            if word in event.raw_text.lower():
                await event.reply(available_keys[word][mood()])