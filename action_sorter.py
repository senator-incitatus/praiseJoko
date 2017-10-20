#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sorts the incoming commands.
"""

import dict_handler
import level_actions
import object_actions

def actionSorter(action, num):
    """
    Handles the incoming action, and does something useful with it!
    Arg values for level actions:
    4 - levelDict, stateDict, num
    3 - levelDict, stateDict
    2 - stateDict
    1 - levelDict
    0 - no args
    Most object commands are executed using the function basicCommands
    Saving & praising work differently.
    """
    lvlcmdDict = dict_handler.getCommands("levelCommands")
    objcmdDict = dict_handler.getCommands("objectCommands")
    invcmdDict = dict_handler.getCommands("inventoryCommands")
    levelDict = dict_handler.getLevel(num)
    stateDict = dict_handler.getState(num)

    actionList = action.split()
    num = str(num)
    try:
        action = actionList[0].lower()
    except IndexError:
        print("Choose an action to perform")
    if action in lvlcmdDict and action != "args":
        levelAction = lvlcmdDict[action]
        callTo = getattr(level_actions, levelAction)
        for key, value in lvlcmdDict["args"].items():
            if key == levelAction:
                if value == 4:
                    callTo(levelDict, stateDict, num)
                elif value == 3:
                    callTo(levelDict, stateDict)
                elif value == 2:
                    callTo(stateDict)
                elif value == 1:
                    callTo(levelDict)
                else:
                    callTo()
    elif action in objcmdDict:
        if action == "save":
            try:
                level_actions.save(actionList[1])
            except IndexError:
                level_actions.save()
        elif action == "praise":
            try:
                if actionList[1]:
                    if actionList[1].lower() != "joko":
                        print("Heretic! You cannot praise anything but Joko!")
                    else:
                        level_actions.praiseJoko(levelDict, stateDict, num)
            except IndexError:
                level_actions.praiseJoko(levelDict, stateDict, num)
        else:
            objectAction = objcmdDict[actionList[0]]
            try:
                if actionList[1]:
                    focus = " ".join(actionList[1:])
                    focus = focus.capitalize()
                    if objectAction == "drop" or objectAction == "use":
                        objDict = dict_handler.objectDropped(focus, objectAction)
                    elif objectAction == "take":
                        objDict = dict_handler.objectTake(focus, num)
                    else:
                        objDict = dict_handler.objectChecker(focus, levelDict, stateDict)
                    if objDict:
                        object_actions.basicCommands(objectAction, objDict, stateDict, num)
            except IndexError:
                print("You need to specify an object to interact with.")
    elif action in invcmdDict:
        print("inv")
    elif action:
        print("That is not a valid command.")
