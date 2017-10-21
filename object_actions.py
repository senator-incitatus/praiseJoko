#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Functions for all "object" commands.
"""

import game
import dict_handler

def basicCommands(command, objDict, stateDict, num):
    """
    Processes the object commands, and in case of the few "special" ones, sends them along to their second destination.
    """
    if command == "take" and "take" in objDict["commands"]:
        itemTake(objDict, stateDict, num)
    elif command == "drop" and "drop" in objDict["commands"]:
        target = objDict["itemName"]
        itemDrop(target, num)
    elif command == "use" and "use" in objDict["commands"]:
        itemUse(objDict, num, stateDict)
    elif command in objDict["commands"]:
        try:
            thing = objDict["thing"]
            if objDict["key"] == command and stateDict["objects"][thing]["keyAction"] is False:
                keyAction(objDict, num)
            elif objDict["key"] is not command:
                if command == "kick" and stateDict["objects"][thing]["inInv"] is True:
                    print("You cannot kick an object you are carrying.")
                else:
                    print(objDict[command])
        except KeyError:
            if command == "kick" and stateDict["objects"][thing]["inInv"] is True:
                print("You cannot kick an object you are carrying.")
            else:
                print(objDict[command])
        try:
            if command == "kick" and objDict["whenDone"] == "allDone":
                data = game.readSession()
                data["gameStats"]["kicks"] += 1
                game.writeSession(data)
        except KeyError:
            pass
        try:
            if command == "kick" and objDict["breaks"] is True:
                data = game.readSession()
                data["levels"][num]["objects"][thing]["visibility"] = -1
                game.writeSession(data)
        except KeyError:
            pass
    else:
        print("Joko forbids you from doing this with {target}. Shame on you for trying.".format(
            target=objDict["itemName"]
        ))

def keyAction(objDict, num):
    """
    Handles increasing the state and such.
    """
    thing = objDict["thing"]
    data = game.readSession()
    activeLevel = data["levels"][num]
    activeLevel["state"] += 1
    activeLevel["objects"][thing]["keyAction"] = True
    if objDict["whenDone"] != "allDone":
        revealed = objDict["whenDone"]
        if isinstance(revealed, list):
            for item in revealed:
                activeLevel["objects"][item]["visibility"] = 1
        else:
            activeLevel["objects"][revealed]["visibility"] = 1
    else:
        activeLevel["allDone"] = True
    data["levels"][num] = activeLevel
    game.writeSession(data)
    print("\n" + objDict["keyAction"])

def keyActionUse(objDict, num):
    """
    Again, the problem with doing things with inventory items on a level they didn't originate from.
    """
    thing = objDict["thing"]
    level = objDict["level"]
    data = game.readSession()
    activeLevel = data["levels"][num]
    activeLevel["state"] += 1
    objLevel = data["levels"][level]
    objLevel["objects"][thing]["keyAction"] = True
    if objDict["whenDone"] != "allDone":
        revealed = objDict["whenDone"]
        if isinstance(revealed, list):
            for item in revealed:
                activeLevel["objects"][item]["visibility"] = 1
        else:
            activeLevel["objects"][revealed]["visibility"] = 1
    else:
        activeLevel["allDone"] = True
    data["levels"][num] = activeLevel
    data["levels"][level] = objLevel
    game.writeSession(data)
    print("\n" + objDict["keyAction"])

def itemTake(objDict, stateDict, num):
    """
    Places an item in your inventory.
    """
    inventory = objDict["inventory"]
    name = objDict.pop("itemName", None)
    data = game.readSession()
    if name in data["inventory"]:
        print("You've already picked this up.")
    elif name in data["dropped"]:
        ohJoy = data["dropped"]
        data["inventory"][name] = ohJoy.pop(name, None)
        level = data["inventory"][name]["level"]
        objectKey = data["inventory"][name]["key"]
        levelObjects = data["levels"][level]["objects"]
        levelObjects[objectKey]["inInv"] = True
        print(data["inventory"][name]["take"])
        game.writeSession(data)
    else:
        thing = objDict["thing"]
        data["levels"][num]["objects"][thing]["inInv"] = True
        data["inventory"][name] = inventory
        game.writeSession(data)
        try:
            if objDict["key"] == "take" and stateDict["objects"][thing]["keyAction"] is False:
                keyAction(objDict, num)
            elif stateDict["objects"][thing]["keyAction"] is True:
                print(objDict["take"])
            else:
                print(objDict["take"])
        except KeyError:
            print(objDict["take"])

def itemDrop(target, num):
    """
    Removes an item from your inventory.
    """
    data = game.readSession()
    inventory = data["inventory"]
    data["dropped"][target] = inventory.pop(target, None)
    try:
        data["dropped"][target]["droppedAt"] = num
        level = data["dropped"][target]["level"]
        objectKey = data["dropped"][target]["key"]
        levelObjects = data["levels"][level]["objects"]
        levelObjects[objectKey]["inInv"] = False
        if data["dropped"][target]["droppedAt"] != data["dropped"][target]["level"]:
            levelObjects[objectKey]["droppedElsewhere"] = True
        game.writeSession(data)
        print(data["dropped"][target]["drop"])
    except TypeError:
        print("You cannot drop what you aren't carrying.")

def itemUse(objDict, level, stateDict):
    """
    Checks if you can use your item. Uses it if you can!
    """
    objStateDict = dict_handler.getState(objDict["inventory"]["level"])
    key = objDict["inventory"]["key"]
    objStateDict = objStateDict["objects"][key]
    useDict = objDict["inventory"]["invUse"]
    if useDict["onLevel"] == level:
        try:
            if useDict["key"] == "use":
                if objDict["itemName"] == "smelly sock":
                    objStateDict["keyAction"] = False
                if objStateDict["keyAction"] is False and stateDict["state"] >= useDict["state"]:
                    keyActionUse(useDict, level)
                else:
                    print(useDict["use"])
            else:
                print(useDict["use"])
        except KeyError:
            print(useDict["use"])
    else:
        print("You can't use that here.")
