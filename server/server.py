import logging
from threading import Lock

from gameauth import TokenValidator, InvalidTokenError
from gamecomm.server import WsGameListener, GameConnection

from .manager import MyManager

logger = logging.getLogger(__name__)


class MyServer:
    
    def __init__(self, local_ip, local_port, token_validator: TokenValidator):
        self.local_ip = local_ip
        self.local_port = local_port
        self.token_validator = token_validator
        self._managers: dict[str, MyManager] = {}
        self._lock = Lock()
    
    # creates or finds manager
    def _find_or_create_manager(self, gid: str):
        with self._lock:
            if gid not in self._managers:
                self._managers[gid] = MyManager(gid)
                logger.info(f"created new manager for gid {gid}")
            return self._managers[gid]

    # handles the authentication
    def handle_authentication(self, gid: str, token: str):
        try:
            return self.token_validator.validate(gid, token)
        except InvalidTokenError:
            return None

    # creates a manager based on gid and handles connection
    def handle_connection(self, connection):
        manager = self._find_or_create_manager(connection.gid)
        manager.handle_connection(connection)

    def handle_stop(self):
        with self._lock:
            for manager in self._managers.values():
                manager.stop()

    # runs server
    def run(self):
        logger.info(f"listening on {self.local_ip}:{self.local_port}")
        logger.info(f"authentication is {'enabled' if self.token_validator else 'disabled'}")
        listener = WsGameListener(self.local_ip, self.local_port,
                                  on_connection=self.handle_connection,
                                  on_authenticate=self.handle_authentication if self.token_validator else None,
                                  on_stop=self.handle_stop)
        listener.run()