import logging
import requests

from requests.auth import HTTPBasicAuth
from requests.compat import urljoin

from .errors import AuthenticationRequiredError

import time


logger = logging.getLogger(__name__)


class UsersApiClient:
    
    USERS_PATH = "/users"
    
    def __init__(self, base_url):
        self.base_url = base_url
        self._auth = None
        
    def auth(self, uid: str, password: str):
        self._auth = HTTPBasicAuth(uid, password)
    
    # joins the wait list in the rest api
    def join_waiting_list(self, login):
        url = urljoin(self.base_url, self._href_for_uid(login["uid"]))
        response = requests.post(url, json=login)
        response.raise_for_status()
        return response.json()
    # creates use in database
    def create_user(self, data: dict):
        url = urljoin(self.base_url, self.USERS_PATH)
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json(), response.headers.get("ETag")

    # converts string to appropriate url
    def _href_for_uid(self, uid: str, suffix: str = None):
        href = f"{self.USERS_PATH}/{uid}"
        if suffix:
            href = f"{href}/{suffix}"
        return href
    # gets user info
    def fetch_user(self, data : dict):
        uid = data["uid"]
        url = urljoin(self.base_url, self._href_for_uid(uid))
        response = requests.get(url, json=data)
        # if the user wasn't found return None instead of raising an error
        if response.status_code == 404:
            return None
        if response.status_code == 201:
            return "incorrect password"
        response.raise_for_status()
        return response.json(), response.headers.get("ETag")
    # delets user
    def delete_user(self, uid: str):
        if not self._auth:
            raise AuthenticationRequiredError()
        url = urljoin(self.base_url, self._href_for_uid(uid))
        response = requests.delete(url, auth=self._auth)
        response.raise_for_status()
    # changes password
    def change_password(self, uid: str, password: str):
        if not self._auth:
            raise AuthenticationRequiredError()
        url = urljoin(self.base_url, self._href_for_uid(uid, "password"))
        response = requests.put(url, data=password, auth=self._auth)
        response.raise_for_status()
