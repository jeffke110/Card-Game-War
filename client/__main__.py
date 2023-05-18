import argparse
import logging
import sys
import logging
from requests.exceptions import HTTPError


from .errors import AuthenticationRequiredError
from .users_api_client import UsersApiClient
from .games_api_client import GamesApiClient
from .game_api_handler import GameApiHandler

from .client import WarClient
import time

logger = logging.getLogger(__name__)

import argparse
import time
from typing import List, Dict, Any, Optional

import requests


class ClientLauncher:
    DEFAULT_URL = "http://127.0.0.1:10021"

    def __init__(self, url: str = DEFAULT_URL):
        self.api_client = UsersApiClient(url)
        self.api_game = GamesApiClient(url)
        self.game_handle = GameApiHandler(self.api_game)
        self.recv_json = None
        self.username = None
        self.password = None

    # runs command line interface for rest api
    def run(self):
        print("\nWelcome to War: the Card Game\nSign up/Log in")
        self._create_or_authenticate_user()
        print("type 'join_game' to join a game")
        print("type 'change_password' to change password")
        print("type 'delete_user' to delete user")
        while True:
            command = input("type command here: ")
            if command == "join_game":
                created_game = self._join_game()
                if created_game:
                    token = created_game["token"]
                    url = created_game["server"]
                    war_client = WarClient()
                    war_client.connect_to_server(url, token, created_game)
                    if created_game["creator"] == self.username:
                        self.api_game.delete_game(created_game["gid"])
            elif command == "change_password":
                self._change_password(self.username)
            elif command == "delete_user":
                self._delete_user(self.username)
                break
            else:
                print("Incorrect input")

    # gets username and password from command line
    def _get_user_credentials(self):
        username = input("input username: ")
        password = input("input password: ")
        return username, password

    # creates or fetches user, error if password is incorrect
    def _create_or_authenticate_user(self):
        done = False
        while done == False:
            self.username, self.password = self._get_user_credentials()
            self.recv_json = self.api_client.fetch_user({"uid": self.username, "password": self.password})
            if self.recv_json == "incorrect password":
                print("ERROR: incorrect password/user has same uid")
                done = False
            elif self.recv_json is None:
                self.api_client.create_user({"uid": self.username, "password": self.password})
                print("user created")
                self.api_client.auth(self.username, self.password)
                done = True
            else:
                print("user found")
                self.api_client.auth(self.username, self.password)
                print(self.recv_json)
                done = True

    # joins a game (waits for another player to join)
    def _join_game(self):
        print("Waiting for another player to join..")
        waiting_list = self.api_client.join_waiting_list({"uid": self.username, "password" : self.password})
        if waiting_list is None:
            print("no waiting users found within 120 seconds")
            return None
        else:
            return self._create_join_game(waiting_list)

    # creates a game or joins a game
    def _create_join_game(self, waiting_users: List[str]):
        if len(waiting_users) == 1:
            print("Game Found!: joining game")
            time.sleep(0.1)
            game = self.game_handle.create_game(waiting_users, 1)
        else:
            print("Game Found!: joining game")
            game = self.game_handle.create_game(waiting_users, 2)
        return game

    # changes the password
    def _change_password(self, username: str):
        print("change_password")
        new_password = input("type in new password:")
        self.api_client.change_password(username, new_password)

    # deletes a user
    def _delete_user(self, username: str):
        print("delete_user")
        self.api_client.delete_user(username)

def parse_args():
    parser = argparse.ArgumentParser(prog="client")
    parser.add_argument("--url", type=str, default=ClientLauncher.DEFAULT_URL, help="base URL for the API")
    parser.add_argument("--log-level", type=str, default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="set the logging level")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    logging.basicConfig(level=args.log_level,
                        format="%(asctime)s %(levelname)s %(name)s %(threadName)s %(message)s")
    ClientLauncher(args.url).run()
