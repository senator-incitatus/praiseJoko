#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Help file for handling dicts.
"""

import game

def getLevel(num):
    """
    Get the dict for the appropriate level
    """
    num = str(num)
    levelDict = dict()
    data = game.readSession("schema/levels.json")
    for key, value in data.items():
        if key == num:
            levelDict = value
    return levelDict

def getState(num):
    """
    Get the dict of the player state.
    """
    num = str(num)
    stateDict = dict()
    save = game.readSession()
    for key, value in save.items():
        if key == "levels":
            for k, level in value.items():
                if k == num:
                    stateDict = level
    return stateDict

def getCommands(commandType):
    """
    Compiles commands, for easy reference.
    """
    cmdDict = dict()
    data = game.readSession("schema/info.json")
    for key, value in data.items():
        if key == commandType:
            cmdDict = value
    return cmdDict

def objectChecker(target, levelDict, stateDict):
    """
    Verifies whether the object interacted with exists on the specified level, and is visible.
    Returns the object dictionary if it exists.
    """
    objDict = dict()
    for thing, states in stateDict["objects"].items():
        thing = int(thing)
        for key in levelDict["objects"][thing].keys():
            if key.lower() == target.lower():
                if states["visibility"] is 1:
                    objectKey = key
                    thingKey = thing
    try:
        for li in levelDict["objects"]:
            for item, value in li.items():
                if item == objectKey:
                    objDict = value
                    objDict["thing"] = str(thingKey)
                    objDict["itemName"] = target.lower()
        return objDict
    except UnboundLocalError:
        msg = "I'm not quite sure what you're looking at, or trying to do with that,"
        msg2 = "for whatever it is, it's not here."
        print("{msg1} {msg2}".format(
            msg1=msg,
            msg2=msg2
        ))

def objectDropped(target, action):
    """
    Since dropped objects don't always get dropped on their level,
    we have to deal with it separately. Also, handy for use-items.
    """
    tempDict = dict()
    data = game.readSession()
    inventory = data["inventory"]
    item = target.lower()
    for thing, values in inventory.items():
        if thing == item:
            tempDict = values
    try:
        level = tempDict["level"]
        levelDict = getLevel(level)
        stateDict = getState(level)
        objDict = objectChecker(item, levelDict, stateDict)
        return objDict
    except KeyError:
        if action == "drop":
            print("You cannot drop what you aren't carrying.")
        elif action == "use":
            print("You can't use something you haven't got.")

def objectTake(target, level):
    """
    Because inventory just made things complicated.
    """
    tempDict = dict()
    data = game.readSession()
    target = target.lower()
    dropped = data["dropped"]
    for thing, values in dropped.items():
        if thing == target:
            tempDict = values
    if not tempDict:
        stateDict = getState(level)
        levelDict = getLevel(level)
        objDict = objectChecker(target, levelDict, stateDict)
    elif tempDict["droppedAt"] == level:
        orgLevel = int(tempDict["level"])
        stateDict = getState(orgLevel)
        levelDict = getLevel(orgLevel)
        objDict = objectChecker(target, levelDict, stateDict)
    try:
        return objDict
    except UnboundLocalError:
        print("What you're trying to pick up isn't here.")
