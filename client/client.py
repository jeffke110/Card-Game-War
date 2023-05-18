from gamecomm.client import GameClient
from .game_client import MyGameClient
from .gui import WarGameGUI
from .sound import Sound
import time
import pygame
import sys
from pygame.locals import *

import logging

logger = logging.getLogger(__name__)

background_green = (0, 128, 0)
background_red = (128, 0, 0)

class WarClient:
    
    def __init__(self):
        self.client = None
        self.done = False
        self.opponent_name = None
        self.player_name = None
        self.gui = None
        self.sound = None
        self.start = False
        self.opponent_move = False
    
    # handles making a move from the client
    def move(self):
        message = {"move": ""}
        self.client.send_message(message)
        logger.info("Waiting for player response...")
        self.gui.waiting_for_player(self.opponent_move)
        self.sound.player_flip()
    
    # handles all game events from server
    def handle_event(self, event: dict):
        # Dispatch to appropriate method based on event type
        if event["event"] == "end of game":
            self.handle_end_of_game(event)
        elif event["event"] == "result":
            self.handle_result(event)
        elif event["event"] == "war":
            self.handle_war(event)
        elif event["event"] == "start":
            self.handle_player_init(event)
        elif event["event"] == "opponent":
            self.handle_opponent()
    
    #handles gui for opponent
    def handle_opponent(self):
        self.opponent_move = True
        self.gui.handle_opponent()
        self.sound.player_flip()
    
    # sets players name and opponents name
    def handle_player_init(self, event):
        self.player_name = event["player"]
        self.opponent_name = event["opponent"]
    
    # handles the gui for the end of game and variables
    def handle_end_of_game(self, event: dict):
        if self.opponent_move == False:
            self.gui.handle_opponent()
        time.sleep(3)
        self.gui.screen.fill((background_green))
        self.gui.player_display_card(event["player"])
        self.gui.opponent_display_card(event["opponent"])
        self.gui.display_end(event["message"])
        self.opponent_move = False
        if event["player"][0] == event["winner"]:
            self.sound.play_win()
        else:
            self.sound.play_lose()
        logger.info(event)
        time.sleep(10)
        self.done = True
    
    #handles the result from a round and displays on gui
    def handle_result(self, event: dict):
        if self.opponent_move == False:
            self.gui.handle_opponent()
        time.sleep(3)
        self.gui.screen.fill((background_green))
        self.gui.player_display_card(event["player"])
        self.gui.opponent_display_card(event["opponent"])
        self.gui.display_result(event["result"])
        self.opponent_move = False
        if event["player"][0] == event["result"]:
            self.sound.play_win()
        else:
            self.sound.play_lose()
        logger.info(event)
        time.sleep(3)
        self.gui.click_card_instruction()
        self.gui.display_card_backs()
        self.gui.can_click = True

    # handles the gui for war
    def handle_war(self, event: dict):
        if self.opponent_move == False:
            self.gui.handle_opponent()
        time.sleep(3)
        self.gui.screen.fill((background_red))
        self.gui.display_war_cards(event["war count"])
        self.gui.player_display_card(event["player"])
        self.gui.opponent_display_card(event["opponent"])
        self.gui.display_war()
        self.sound.play_war()
        logger.info(event)
        time.sleep(3)
        self.gui.click_card_instruction()
        self.gui.display_card_backs()
        self.gui.can_click = True
           
    # connects to the server given the url 
    def connect_to_server(self, url, token, info):
        self.client = MyGameClient(url, token, self.handle_event, info)
        self.client.start()
        self.gui = WarGameGUI()
        self.sound = Sound()
        self.setup_gui()
        self.wait_for_input()
    
    # sets up the gui   
    def setup_gui(self):
        self.gui.screen.fill((background_green))
        self.gui.handle_player_init(self.player_name, self.opponent_name)
        self.gui.display_card_backs()
        self.gui.click_card_instruction()
    
    # waits for input from the user
    def wait_for_input(self):
        clock = pygame.time.Clock()
        while not self.done:
            clock.tick(60)  # Limit the frame rate to 60 FPSs
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and self.gui.can_click == True:
                    if self.gui.is_within_area(pygame.mouse.get_pos(), self.gui.card_area):
                        logger.info("Mouse Clicked Button")
                        self.gui.can_click = False
                        self.move()
                if event.type == pygame.QUIT:
                    self.done = True
        pygame.quit()
        self.client.stop()
