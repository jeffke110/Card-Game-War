import logging
import threading
from threading import Lock
from .hand import Hand
from .card import Card

from gamecomm.server import GameConnection
logger = logging.getLogger(__name__)

class Player:
    def __init__(self, game_connection: GameConnection):
        self.game_connection = game_connection
        self.move = None
        self.hand = Hand()
        self.curr_card = None
      

class MyPublisher:

    def __init__(self):
        self._subscribers: list[Player] = []
        self._lock = Lock()
        self.done_count = 0
        self.cond = threading.Condition(self._lock)
        self.war_deck: list[Card] = []
        self.in_war = False
        self.war_count = 0
        self.war_wait = 0

    # adds subscriber
    def add_subscriber(self, player: Player):
        logger.info(f"adding subscriber {player.game_connection.uid}")
        with self._lock:
            self._subscribers.append(player)

    # removes subscriber
    def remove_subscriber(self, player: Player):
        logger.info(f"removing subscriber {player.game_connection.uid}")
        with self._lock:
            self._subscribers.remove(player)

    # publishes an event for all subscribers
    def publish_event(self, event):
        logger.info(f"publishing event: {event}")
        with self._lock:
            subscribers = list(self._subscribers)
        for subscriber in subscribers:
            subscriber.game_connection.send(event)
            
