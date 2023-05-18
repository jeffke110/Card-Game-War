import logging
from threading import Event
from typing import Callable
import threading
import time
import json

from .hand import Hand

from gamecomm.server import GameConnection, ConnectionClosedOK, ConnectionClosedError

from .publisher import MyPublisher
from .game_logic import Game_Logic

logger = logging.getLogger(__name__)

class MyController:
    
    # Define a timeout value for receiving data from a connection
    RECV_TIMEOUT_SECONDS = 0.250

    def __init__(self, connection: GameConnection, publisher: MyPublisher,
                 on_close: Callable[[GameConnection], None]):
        # Store references to the GameConnection, MyPublisher, and callback function
        self.connection = connection
        self.publisher = publisher
        self.on_close = on_close
        
        # Create an Event object to signal that the controller should shut down
        self._shutdown = Event()
        
        # Store a reference to the publisher's lock for thread safety
        self._lock = publisher._lock
        
        # Create a Game_Logic object to handle game logic
        self.game_logic = Game_Logic(publisher, connection)

    def wait_for_all_connections(self):
        # Wait for all subscribers to connect to the publisher
        with self._lock:
            subscribers = list(self.publisher._subscribers)
        while(len(subscribers) == 1):
            with self._lock:
                subscribers = list(self.publisher._subscribers)

    def run(self):
        # Log that the controller has connected to the GameConnection
        logger.info(f"connected to {self.connection} for user {self.connection.uid} in game {self.connection.gid}")
        
        # Wait for all subscribers to connect to the publisher
        self.wait_for_all_connections()
        
        # Set the player's opponent in the game logic
        self.game_logic.set_player_opponent()
        
        # Send the player's information to the opponent
        self.game_logic.send_player_info()
        
        try:
            # Loop until the controller is shutdown
            while not self._shutdown.is_set():
                # Receive data from the GameConnection
                request = self.connection.recv(self.RECV_TIMEOUT_SECONDS)
                logger.info(f"received request: {request}")
                
                # Handle the received data and send a response
                response = self.handle_request(request)
                self.connection.send(response)
        except ConnectionClosedOK:
            # The connection was closed intentionally, so just exit the loop
            pass
        except ConnectionClosedError as err:
            # An error occurred communicating with the client, log the error
            logger.error(f"error communicating with client: {err}")
        
        # Call the on_close callback function
        self.on_close(self.connection)
        
        # Log that the controller has disconnected from the GameConnection
        logger.info(f"disconnected from {self.connection} for user {self.connection.uid} in game {self.connection.gid}")

    def stop(self):
        # Signal the controller to shutdown
        logger.info("handling stop")
        self._shutdown.set()
                
    def handle_request(self, message: dict):
        # Handle the request based on the type of message received
        if "move" in message.keys():
            # If the message is a move, set the move in the game logic and start a new round
            self.game_logic.set_move(message["move"])
            return self.game_logic.set_up_round() 
                           
    
    