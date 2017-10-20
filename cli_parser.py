#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Parsing CLI options via argparse.
"""

import argparse
import json
import sys
import game

VERSION = "v1.0.0 (2017-10-16)"

options = {}

def parse_options():
    """
    Parse all command line options and arguments and return them as a dictionary.
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("-v", "--version", action="version", version=VERSION)

    parser.add_argument("-i", "--info", dest="info",
                        action="store_true", default=False, help="info about the game")
    parser.add_argument("-a", "--about", dest="about",
                        action="store_true", default=False, help="info about the game's author")
    parser.add_argument("-c", "--cheat", dest="cheat",
                        action="store_true", default=False, help="gives you the shortest route to completing the game")

    args, unknownargs = parser.parse_known_args()

    readOut = ""
    for arg in vars(args):
        if vars(args)[arg]:
            readOut = arg

    if readOut:
        with open("schema/info.json") as jsonData:
            data = json.load(jsonData)
            for item in data[readOut]:
                print(item)

    if not len(sys.argv) > 1:
        game.start()

    options["known_args"] = vars(args)
    options["unknown_args"] = unknownargs

    return options
