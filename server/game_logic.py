
import logging
from threading import Event
from typing import Callable
from gamecomm.server import GameConnection
from .publisher import MyPublisher

logger = logging.getLogger(__name__)


class Game_Logic:
    def __init__(self, publisher: MyPublisher, connection: GameConnection):
        self.connection = connection
        self.publisher = publisher
        self._lock = publisher._lock
        self.war_deck = publisher.war_deck
        self.in_war = publisher.in_war
        self.war_count = publisher.war_count
        self.player = None
        self.opponent = None
    
    # set player and opponent information
    def set_player_opponent(self):
        with self._lock:
            subscribers = self.publisher._subscribers
        for subscriber in subscribers:
            if self.connection.uid == subscriber.game_connection.uid:
                self.player =  subscriber
            else:
                self.opponent = subscriber
    
    # set move
    def set_move(self, move):
        with self._lock:
            if(len(self.player.hand) > 0):
                self.player.curr_card = self.player.hand.pop()
            else:
                self.player.curr_card = None
            self.player.move = move
    
    # calculates and executes each round
    def execute_round(self):
        with self._lock:
            player_name = self.player.game_connection.uid
            opponent_name = self.opponent.game_connection.uid
            player_hand = self.player.hand
            opponent_hand = self.opponent.hand
            result = ""
            if(len(player_hand) >= 0 and len(opponent_hand) >= 0 
               and self.player.curr_card is not None
               and self.opponent.curr_card is not None):
                    player_card = self.player.curr_card
                    opponent_card = self.opponent.curr_card
                    if(player_card.rank > opponent_card.rank):
                        if self.in_war:
                            result = player_name
                            player_hand.cards.extend(self.war_deck)
                            player_hand.push(player_card)
                            player_hand.push(opponent_card)
                            self.war_deck.clear()
                            self.in_war = False
                            self.war_count = 0
                        else:
                            result = player_name
                            player_hand.push(player_card)
                            player_hand.push(opponent_card)
                    elif(player_card.rank < opponent_card.rank):
                        if self.in_war:
                            result = opponent_name
                            self.in_war = False
                            self.war_count = 0
                        else:
                            result = opponent_name
                    else:
                        # war
                        result = self.war_logic()
            
            self.publisher.done_count = self.publisher.done_count + 1
            if self.publisher.done_count == 2:
                self.publisher.cond.notify_all()
            return result
    
    # waits for decks to be changed so that clients display correct info
    def wait_changed_decks(self):
        with self._lock:
            while self.publisher.done_count < 2:
                self.publisher.cond.wait()
    
    # waits for both players  
    def wait_for_player_move(self):
        sent = False
        with self._lock:
            self.publisher.done_count = 0
            self.publisher.war_wait = 0
            subscribers = list(self.publisher._subscribers)
        player1_move = None
        player2_move = None
        # wait for both players move
        while (player1_move == None or  player2_move == None):
            with self._lock:
                player1_move = subscribers[0].move
                player2_move = subscribers[1].move
                if (player1_move == None or  player2_move == None) and sent == False:
                    self.opponent.game_connection.send({"event" : "opponent"})
                    sent = True
    # waits for war cards to be edited
    def wait_war_cards(self, result):
        if result == "war":
            with self._lock:
                while self.publisher.war_wait < 2:
                    self.publisher.cond.wait()

    # sets up and takes care of all the round execution
    def set_up_round(self):
        
        self.wait_for_player_move()
        result = self.execute_round()
        self.wait_changed_decks()
        self.set_player_opponent()
        with self._lock:
            if result == "war":
                self.war_deck.append(self.player.curr_card)
                self.war_deck.append(self.player.hand.pop())
                self.war_deck.append(self.player.hand.pop())
                self.war_deck.append(self.player.hand.pop())
                self.publisher.war_wait = self.publisher.war_wait + 1
                if self.publisher.war_wait == 2:
                    self.publisher.cond.notify_all()
                    
        self.wait_war_cards(result)
        output = self.output_end(result)
        self.player.move = None
        self.opponent.move = None
        self.player.hand.shuffle()
        if output is not None:
            return output
        elif self.in_war:
            return self.war_output()
        else:
            data = self.round_output(result)
            return data
    
    # returns round output
    def round_output(self, result):
        data = {"event": "result", "result" : result, 
                "player" : [self.player.game_connection.uid,
                            f"{self.player.curr_card.suit}", 
                            f"{self.player.curr_card.rank}", 
                            f"{len(self.player.hand)}"], 
                "opponent": [ self.opponent.game_connection.uid,
                             f"{self.opponent.curr_card.suit}",
                             f"{self.opponent.curr_card.rank}",
                             f"{len(self.opponent.hand)}"], 
                "status" : "ok"}
        
        return data

    # game logic for war
    def war_logic(self):
        self.in_war = True
        if(len(self.player.hand) > 3 and len(self.opponent.hand) > 3):
            self.war_count = self.war_count + 1
            return "war"
        if(len(self.player.hand) <= 3 and len(self.opponent.hand) <= 3):
            self.in_war = False
            return "tie in War: both players don't have enough cards for War"
        if(len(self.player.hand) <= 3):
            self.in_war = False
            return "opponent wins: not enough cards for War"
        if(len(self.opponent.hand) <= 3):
            self.in_war = False
            return "player wins: not enough cards for War"
        else:
            return "tie in War"
    # special output when there is war 
    def war_output(self):
        data = {"event": "war",
                "war count" : f"{self.war_count}",
                "player" : [self.player.game_connection.uid,
                            f"{self.player.curr_card.suit}", 
                            f"{self.player.curr_card.rank}", 
                            f"{len(self.player.hand)}"], 
                "opponent": [ self.opponent.game_connection.uid,
                             f"{self.opponent.curr_card.suit}",
                             f"{self.opponent.curr_card.rank}",
                             f"{len(self.opponent.hand)}"], 
                "status" : "ok"}
        return data
    # sends when opponent makes a move
    def send_player_info(self):
        data = {"event": "start",
                "player" : self.player.game_connection.uid,
                "opponent": self.opponent.game_connection.uid,
                "status" : "ok"}
        self.connection.send(data)
    # returns output when the game is over
    def output_end(self, result):
        message = None
        winner = None
        if result == "player wins: not enough cards for War":
            message = f"{self.player.game_connection.uid} wins game: not enough cards for war"
            winner =  f"{self.player.game_connection.uid}"
        elif result == "opponent wins: not enough cards for War":
            message = f"{self.opponent.game_connection.uid} wins game: not enough cards for war"
            winner =  f"{self.opponent.game_connection.uid}"
        elif self.player.hand.is_empty():
           message = f"{self.opponent.game_connection.uid} wins"
           winner =  f"{self.opponent.game_connection.uid}"
        elif self.opponent.hand.is_empty():
            message = f"{self.player.game_connection.uid} wins"
            winner =  f"{self.player.game_connection.uid}"
        elif result == "tie in War: both players don't have enough cards for War":
            winner =  f"tie"
            message = f"tie in War: both players don't have enough cards for War"
        if(winner is not None):
            return {"event": "end of game", 
                    "message": message,
                    "winner": winner,
                    "player" : [self.player.game_connection.uid,
                                f"{self.player.curr_card.suit}", 
                                f"{self.player.curr_card.rank}", 
                                f"{len(self.player.hand)}"], 
                    "opponent": [ self.opponent.game_connection.uid,
                                f"{self.opponent.curr_card.suit}",
                                f"{self.opponent.curr_card.rank}",
                                f"{len(self.opponent.hand)}"], 
                    "status" : "ok"}
        else:
            return None