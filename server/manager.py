import logging
from threading import Lock

from gamecomm.server import GameConnection

from .controller import MyController
from .publisher import MyPublisher, Player
from .deck import Deck

logger = logging.getLogger(__name__)


class MyManager:
    """
    This class manages game connections and controllers for a game session.
    """
    def __init__(self, gid: str):
        """
        Initializes the MyManager object with the given game ID (gid), a MyPublisher object for handling 
        publishing/subscribing messages, a dictionary to keep track of game controllers for each connection,
        a lock for thread safety, a deck of cards to be used in the game, and shuffles the deck.
        """
        self.gid = gid
        self.publisher = MyPublisher()
        self._controllers: dict[GameConnection, MyController] = {}
        self._lock = Lock()
        self.deck = Deck()
        self.deck.shuffle()

    def handle_close(self, connection: GameConnection):
        """
        Removes the controller and connection associated with the given connection object from the 
        _controllers dictionary and the subscriber associated with the connection from the publisher's
        _subscribers list.
        """
        with self._lock:
            self._controllers.pop(connection)
            self.publisher._subscribers.pop()

    def handle_connection(self, connection):
        """
        Handles a new connection by creating a new MyController object for it, adding it to the 
        _controllers dictionary, adding the connection to the publisher's subscribers, initializing the 
        game by splitting the deck of cards between players and running the controller object.
        """
        controller = MyController(connection, self.publisher, on_close=self.handle_close)
        with self._lock:
            self._controllers[connection] = controller
            self.publisher.add_subscriber(Player(connection))
            logger.info(f"{self.gid} subscribers count: {len(self.publisher._subscribers)}")
            self.hand_game_init()
        controller.run()
        
    def hand_game_init(self):
        """
        Initializes the game by splitting the deck of cards between players. If there is only one subscriber, 
        all cards are given to that subscriber. If there are two subscribers, half of the deck is given to each 
        subscriber.
        """
        if len(self.publisher._subscribers) == 1:
            self.publisher._subscribers[0].hand.cards = self.deck.cards[:len(self.deck)//2]
        elif len(self.publisher._subscribers) == 2:
            self.publisher._subscribers[1].hand.cards = self.deck.cards[len(self.deck)//2:]

    def stop(self):
        """
        Stops all controllers associated with this manager by calling their stop() method.
        """
        with self._lock:
            for controller in self._controllers.values():
                controller.stop()