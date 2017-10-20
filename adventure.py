#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main file of Incitatus's adventure game.
"""

import sys
import cli_parser

def main():
    """
    Main function for the CLI parsing.
    """

    cli_parser.parse_options()

#    print(cli_parser.options)
#    print(cli_parser.options["known_args"])

#    print()

    sys.exit()

if __name__ == "__main__":
    main()
