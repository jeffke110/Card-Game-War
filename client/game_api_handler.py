import subprocess
import time
import logging

from concurrent.futures import wait as await_futures
from threading import Event
from typing import Sequence
from urllib.parse import urljoin

from .games_api_client import GamesApiClient
from .users_api_client import UsersApiClient

logger = logging.getLogger(__name__)


class GameApiHandler:
    
    def __init__(self, games_api : GamesApiClient):
        self.games_api = games_api

    def create_game(self, players, len):
        """
        Creates a new game instance for the specified players.
        :param players: a sequence (list or tuple) in which each element is a tuple consisting of a player's
            user ID and password
        :return: dict containing details for the game instance
        """
        self.games_api.auth(players[0][0], players[0][1])   # use the first player to authenticate to the games API
        if len == 2:
            return self.games_api.create_game([players[0][0], players[1][0]])
        else:
            return self.games_api.create_game([players[0][0]])
    
