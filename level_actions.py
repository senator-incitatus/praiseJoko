#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Functions for all "level wide" commands.
"""

from shutil import copyfile
from random import randint
import dict_handler
import game
import object_actions

def describe(levelDict, stateDict):
    """
    Takes care of displaying the description etc of a level.
    """
    state = stateDict["state"]
    if stateDict["finished"] is True:
        print("\n" + levelDict["description"][-1])
        print("\n" + levelDict["whenDone"])
    else:
        try:
            print("\n" + levelDict["description"][state])
        except IndexError:
            print("\n" + levelDict["description"][-1])
    print("\n")
    for line in levelDict["image"]:
        print(line)
    print("\n")

def helpMenu():
    """
    Lists all available commands.
    """
    helpDict = dict_handler.getCommands("helpCommands")
    for item in helpDict:
        print(item)

def fwd(stateDict):
    """
    Attemps to move you one level up.
    """
    if stateDict["finished"] is True:
        data = game.readSession()
        data["gameStats"]["level"] += 1
        upOne = data["gameStats"]["level"]
        game.writeSession(data)
        game.level(upOne)
    else:
        print("You have not yet completed this chapter in your story.")

def back():
    """
    Attemps to move you down one level.
    """
    data = game.readSession()
    data["gameStats"]["level"] -= 1
    if data["gameStats"]["level"] == -1:
        print("You are already at the beginning. You can only move forward.")
    else:
        downOne = data["gameStats"]["level"]
        game.writeSession(data)
        game.level(downOne)

def look(levelDict, stateDict):
    """
    Tells you if there's anything worth seeing.
    """
    state = stateDict["state"]
    try:
        print(levelDict["toSee"][state])
    except IndexError:
        print(levelDict["toSee"][-1])

def objects(levelDict, stateDict, num):
    """
    Lists all the (currently visible) objects on a level.
    """
    print("You look around you, and this is what you see:\n")
    data = game.readSession()
    if data["dropped"]:
        dropped = data["dropped"]
        for key, value in dropped.items():
            if value["droppedAt"] == num and value["level"] != num:
                print(key.capitalize() + ": {desc}".format(
                    desc=value["inInv"]
                ))
    for key, value in stateDict["objects"].items():
        if value["visibility"] >= 0 and value["inInv"] is False and value["droppedElsewhere"] is False:
            key = int(key)
            for k, v in levelDict["objects"][key].items():
                print("{item}: {desc}".format(
                    item=k,
                    desc=v["description"]
                ))
def hint(levelDict, stateDict):
    """
    Offers some helpful hints if you get stuck.
    """
    msg = "King Joko is a beloved, benevolent King."
    msg2 = "He is everything, and everywhere. He fills you with divine inspiration..."
    print("{msg1} {msg2}\n".format(
        msg1=msg,
        msg2=msg2
    ))
    state = stateDict["state"]
    try:
        print(levelDict["hint"][state])
    except IndexError:
        print(levelDict["hint"][-1])

def save(savename=""):
    """
    Saves current session to save file.
    """
    if savename:
        if savename[-5:] != ".json":
            print("You need to enter the filename in this format: \"name.json\"")
        else:
            copyfile("saves/currentSession.json", "saves/" + savename)
    else:
        data = game.readSession()
        savename = data["gameStats"]["saveFile"]
        copyfile("saves/currentSession.json", "saves/" + savename)
    print("You succesfully saved your progress to the file " + savename)

def praiseJoko(levelDict, stateDict, num):
    """
    It is so important, to praise Joko.
    """
    praises = dict_handler.getCommands("praises")
    if stateDict["allDone"] is True and stateDict["praised"] is False:
        print(praises["allDone"])
        data = game.readSession()
        data["levels"][num]["praised"] = True
        data["levels"][num]["finished"] = True
        game.writeSession(data)
        print(levelDict["whenDone"])
    elif num == "4":
        game.lastLevel()
    else:
        print("Praise Joko!")
        maxInt = len(praises["PSA"]) - 1
        number = randint(0, maxInt)
        msg = "And in answer to your praise of King Joko, your mind stirs"
        msg2 = "with memory of what you have heard many times before..."
        print("{msg1}, {msg2}".format(
            msg1=msg,
            msg2=msg2
        ))
        print("\n\"" + praises["PSA"][number] + "\"")

def inventory():
    """
    Lists your inventory items.
    """
    data = game.readSession()
    pInventory = data["inventory"]
    print("In your satchel, or on your person, you currently have:\n")
    if pInventory:
        for key, value in pInventory.items():
            print("{key}: {desc}\n".format(
                key=key.capitalize(),
                desc=value["inInv"]
            ))
    else:
        print("You are not carrying anything. You are naked.")

def cheat(levelDict, stateDict, num):
    """
    Automatically clears a level for you.
    """
    data = game.readSession()
    if num == "5":
        print("You cannot cheat here.")
    else:
        i = 0
        for key, value in stateDict["objects"].items():
            try:
                if value["keyAction"] is False:
                    i += 1
                    value["visibility"] = 1
                    value["keyAction"] = True
            except KeyError:
                pass
        stateDict["state"] += i
        stateDict["finished"] = True
        stateDict["allDone"] = True
        stateDict["praised"] = True
        data["levels"][num] = stateDict
        game.writeSession(data)
        if num != "4":
            for item in levelDict["objects"]:
                for key, value in item.items():
                    if "Statue" in key:
                        target = key
            objDict = dict_handler.objectTake(target, num)
            object_actions.itemTake(objDict, stateDict, num)
        print("You have automatically cleared this level.")
