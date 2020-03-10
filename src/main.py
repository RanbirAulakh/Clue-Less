# team: The Plum Professors
# author: Ranbir Aulakh, Michael Knatz, Victoria Palaoro, Parth Jalundhwala
# description:

import platform
import sys
import argparse
from client.client import Client

def main():
    parser = argparse.ArgumentParser(description="Clue-Less Game!")
    parser.add_argument('--type', '-t', help="Start as 'Client' or 'Server'", choices=["server", "client"], required=True)
    args = parser.parse_args()

    if args.type.lower() == "client":
        print("Starting Client...")
        Client().client

main()
