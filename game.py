#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Various game things!
"""

import json
from shutil import copyfile
import sys
import dict_handler
import action_sorter

def start():
    """
    Initates the whole shebang!
    """
    print("Praise Joko! - A game by Incitatus\n")
    with open("schema/info.json") as jsonData:
        data = json.load(jsonData)
        for item in data["introduction"]:
            if not isinstance(data["introduction"][item], list):
                print(data["introduction"][item])
    print("To load a game, type \"load <filename>.json\"")
    print("To start a new game, type \"new <filename>.json\"")
    print("\nDon't forget to save your progress using \"save\"!")
    while True:
        action = input("> ")
        action = action.lower()
        action = action.split()
        if action[0] == "load":
            filename = action[1]
            try:
                copyfile("saves/" + action[1], "saves/currentSession.json")
                startFromLoad(filename)
            except FileNotFoundError:
                print("You did not enter a valid saves file.")
        elif action[0] == "new":
            if action[1][-5:] != ".json":
                print("You need to enter the filename in this format: \"name.json\"")
            else:
                copyfile("schema/game.json", "saves/" + action[1])
                data = readSession("saves/" + action[1])
                data["gameStats"]["saveFile"] = action[1]
                writeSession(data, "saves/" + action[1])
                copyfile("saves/" + action[1], "saves/currentSession.json")
                level(0)
        elif action[0] == "exit":
            break
        else:
            print("You supplied an invalid command.")

def startFromLoad(savename):
    """
    A returning player starting from their save!
    """
    with open("saves/" + savename) as jsonData:
        data = json.load(jsonData)
        level(data["gameStats"]["level"])

def level(num):
    """
    The function dealing with each level.
    """
    action_sorter.actionSorter("d", num)
    print("What do you do?")
    while True:
        action = input("> ")
        if action == "exit":
            break
        else:
            action_sorter.actionSorter(action, num)
    sys.exit()

def readSession(filename="saves/currentSession.json"):
    """
    Reads session data.
    """
    with open(filename, "r") as jsonData:
        data = json.load(jsonData)
    return data

def writeSession(data, filename="saves/currentSession.json"):
    """
    Saves session data.
    """
    with open(filename, "w") as jsonData:
        jsonData.write(json.dumps(data, indent=4))

def lastLevel():
    """
    A, praise be! You're fixing the statue.
    """
    data = readSession()
    kicks = data["gameStats"]["kicks"]
    inventory = data["inventory"]
    statues = list()
    for key, value in inventory.items():
        try:
            if value["type"] == "statue":
                value["origName"] = key
                statues.append(value)
        except KeyError:
            pass
    pieces = len(statues)
    if pieces < 4:
        print("You've dropped pieces of the statue?! How dare you! Go fetch them this instant!")
    else:
        for parts in statues:
            name = parts["origName"]
            key = parts["key"]
            num = parts["level"]
            data["levels"][num]["objects"][key]["inInv"] = False
            data["dropped"][name] = data["inventory"].pop(name, None)
        data["levels"]["5"]["objects"]["0"]["inInv"] = True
        levelDict = dict_handler.getLevel("5")
        wholeStatue = levelDict["objects"][0]
        for key, value in wholeStatue.items():
            statName = key
            statInv = value["inventory"]
        data["inventory"][statName] = statInv
        ending = dict_handler.getCommands("ending")
        print(ending["end"])
        if kicks > 0:
            print(ending["kicks"])
        else:
            print(ending["dialogue"])
        print(ending["endnote"])
        data["gameStats"]["statueDone"] = True
        activeLevel = data["levels"]["4"]
        activeLevel["state"] += 1
        activeLevel["allDone"] = True
        activeLevel["praised"] = True
        activeLevel["finished"] = True
        data["levels"]["4"] = activeLevel
        writeSession(data)
