import logging
import requests
from typing import Any
from urllib.parse import urljoin

from requests.auth import HTTPBasicAuth

from .errors import AuthenticationRequiredError


logger = logging.getLogger(__name__)


class GamesApiClient:
    """
    A client for the Games API.
    """
    GAMES_PATH = "/games"
    def __init__(self, base_url):
        """
        Creates a new instance.
        :param base_url: base URL for the API server
        """
        self.base_url = base_url
        self._auth = None

    def auth(self, uid: str, password: str):
        """
        Sets the authentication details for the API methods that require authentication
        :param uid: user ID
        :param password: password
        """
        self._auth = HTTPBasicAuth(uid, password)

    def create_game(self, players: list, custom: Any = None):
        """
        Creates a game object for a collection of players
        :param players: the players for the game
        :param custom: any additional attributes to store with the game (e.g. in a dict)
        :return: result game representation from the server
        """
        if not self._auth:
            raise AuthenticationRequiredError()
        url = urljoin(self.base_url, self.GAMES_PATH)
        data = {"players": players}
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    
    def delete_game(self, gid: str):
        if not self._auth:
            raise AuthenticationRequiredError()
        path = self.GAMES_PATH + f"/{gid}"
        url = urljoin(self.base_url, path)
        response = requests.delete(url, auth=self._auth)
        if response.status_code == 204:
            print("Game deleted successfully!")
        else:
            print(f"Failed to delete game: {response.text}")
    

    
