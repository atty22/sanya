import time
import json
from core import config


def dump(obj):
    """ Debugging tool """
    for attr in dir(obj):
        print("obj.%s = %r" % (attr, getattr(obj, attr)))


def mood() -> int:
    """
    Returns:
         int: The mood (time of the day: 0 = night, 1 = sleeping, 2 = day)
    """
    hour = int(time.strftime('%H'))
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
        return json.load(open("messages/{section}{file}.json".format(section=section + "/", file=file), encoding="utf-8"))
