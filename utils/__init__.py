from time import strftime
import json
from core import config, sanya
import sqlite3


def dump(obj):
    """ Debugging tool """
    for attr in dir(obj):
        print("obj.%s = %r" % (attr, getattr(obj, attr)))


def mood() -> int:
    """
    Returns:
         int: The mood (time of the day: 0 = night, 1 = sleeping, 2 = day)
    """
    hour = int(strftime('%H'))
    if 0 <= hour < int(config["!HOURS!"]["sleeping"]):
        return 0
    elif int(config["!HOURS!"]["sleeping"]) <= hour < int(config["!HOURS!"]["day"]):
        return 1
    elif int(config["!HOURS!"]["day"]) <= hour < int(config["!HOURS!"]["night"]):
        return 2
    else:
        return 0


def mood_to_words(mood: int) -> str:
    """
    This function transforms a numeric mood to a word (e.g. night).

    Args:
        mood (int):
            The numeric value of the mood. It can be 0, 1 or 2.

    Returns:
        str: A string containing the mood. It can be night, sleeping or day.

    Raises:
        ValueError: If mood argument is not an integer value or it is not 0, 1 or 2.
    """
    moods = {0: "night", 1: "sleeping", 2: "day"}
    if type(mood) is not int:
        raise ValueError("mood must be a integer value")
    elif mood > 2 or mood < 0:
        raise ValueError("mood must be 0, 1 or 2.")
    else:
        return moods[mood]


def get_messages(file: str, section: str = "") -> dict:
    """
    Gets data from the json file in the "messages" folder.

    Args:
        file (str):
            The json file to parse.
        section (str, optional):
            The folder in which the file is placed

    Returns:
        dict: A dictionary containing data from json files.

    Raises:
        ValueError: if the file or the section arguments are not strings.
    """
    if type(file) is not str:
        raise ValueError("file must be a string value")
    if type(section) is not str:
        raise ValueError("section must be a string value")
    else:
        return json.load(
            open("messages/{section}{file}.json".format(section=section + "/", file=file), encoding="utf-8"))


def database(chat_id):
    sql = sqlite3.connect("database.db")
    cur = sql.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS chat ( chat_id INTEGER NOT NULL UNIQUE, active INTEGER DEFAULT 1)")
    sql.commit()
    cur.execute("SELECT * FROM chat WHERE chat_id= '{}'".format(chat_id))
    raw = cur.fetchone()
    if raw is None:
        cur.execute("INSERT INTO chat VALUES ('{}', 1)".format(chat_id))
        sql.commit()
        sql.close()
        return "aggiungo chat a database per poter ricevere messaggi casuali"
    else:
        if raw[1] == False:
            cur.execute("UPDATE chat SET active = 1 WHERE chat_id = '{}'".format(chat_id))
            sql.commit()
            sql.close()
            return "la chat è già stata aggiunta in passato ma è stata disattivata, la ho riattivata"
        elif raw[1] == True:
            cur.execute("UPDATE chat SET active = 0 WHERE chat_id = '{}'".format(chat_id))
            sql.commit()
            sql.close()
            return "la chat è già stata attivata, quindi la ho disattivata"
        else:
            sql.close()
            return "coglione"

