import pygame
import sys
from pygame.locals import *
import random

background_green = (0, 128, 0)

class WarGameGUI:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont(None, 30)
        self.clock = pygame.time.Clock()
        self.screen.fill(background_green)
        self.annoucement = ""
        self.can_click = True
            
        self.card_back = pygame.image.load("cards/cardback.png")
        self.read_card = pygame.image.load("cards/readycard.png")
        self.card_images = {}
        self.shuffler = []
        self.create_deck_images()
    
        self.card_coords = (350, 400)
        self.card_width = 100
        self.card_height = 140
        self.card_area = (self.card_coords[0], self.card_coords[1], self.card_width, self.card_height)
    
    # loads all card images from deck
    def create_deck_images(self):
        for suit in ["Hearts", "Diamonds", "Clubs", "Spades"]:
            for rank in range(2, 15):
                if suit == "Hearts":
                    filename = f"cards/{rank}h.png"
                if suit == "Diamonds":
                    filename = f"cards/{rank}d.png"
                if suit == "Clubs":
                    filename = f"cards/{rank}c.png"
                if suit == "Spades":
                    filename = f"cards/{rank}s.png"
                self.card_images[(suit, rank)] = pygame.image.load(filename)
                self.shuffler.append(pygame.image.load(filename))
    
    # loads players name and deck size beginning of game
    def handle_player_init(self, player, opponent):
        player_name = self.font.render(player, True, (0, 0, 0))
        text_pos = player_name.get_rect(center=(self.width//2, 575))
        self.screen.blit(player_name, text_pos)
        
        hand_length = self.font.render(f"cards in deck {26}", True, (0, 0, 0))
        text_pos = hand_length.get_rect(center=(self.width//4, 575))
        self.screen.blit(hand_length, text_pos)
        
        player_name = self.font.render(opponent, True, (0, 0, 0))
        text_pos = player_name.get_rect(center=(self.width//2, 25))
        self.screen.blit(player_name, text_pos)
        
        hand_length = self.font.render(f"cards in deck {26}", True, (0, 0, 0))
        text_pos = hand_length.get_rect(center=(self.width//4, 25))
        self.screen.blit(hand_length, text_pos)    
        
        pygame.display.update()
     
    # handles when an opponent makes a move   
    def handle_opponent(self):
        self.clear_center_text()
        self.screen.blit(self.read_card, (350, 50))
        self.result  = self.font.render("Opponent made a move", True, (0, 0, 0))
        self.annoucement = "Opponent made a move"
        text_pos = self.result.get_rect(center=(self.width//2, self.height//2))
        self.screen.blit(self.result, text_pos)
        pygame.display.update()
    
    # displays players card, name, and amount of cards in deck 
    def player_display_card(self, message : list):
        name = message[0]
        card_suit = message[1]
        card_rank = int(message[2])
        length = message[3]
        
        player_name = self.font.render(name, True, (0, 0, 0))
        text_pos = player_name.get_rect(center=(self.width//2, 575))
        self.screen.blit(player_name, text_pos)
        
        hand_length = self.font.render(f"cards in deck {length}", True, (0, 0, 0))
        text_pos = hand_length.get_rect(center=(self.width//4, 575))
        self.screen.blit(hand_length, text_pos)
        
        card_image = self.card_images[(card_suit, card_rank)]
        self.screen.blit(card_image, (350, 420))
        pygame.display.update()
    
    # displays the opponent card, name, and amount of cards in deck 
    def opponent_display_card(self, message : list):
        name = message[0]
        card_suit = message[1]
        card_rank = int(message[2])
        length = message[3]
        
        player_name = self.font.render(name, True, (0, 0, 0))
        text_pos = player_name.get_rect(center=(self.width//2, 25))
        self.screen.blit(player_name, text_pos)
        
        hand_length = self.font.render(f"cards in deck {length}", True, (0, 0, 0))
        text_pos = hand_length.get_rect(center=(self.width//4, 25))
        self.screen.blit(hand_length, text_pos)
        
        card_image = self.card_images[(card_suit, card_rank)]
        self.screen.blit(card_image, (350, 40))
        pygame.display.update()
    
    #displays the card backs for the game
    def display_card_backs(self):
        card_image = self.card_back
        self.screen.blit(card_image, (350, 420))
        self.screen.blit(card_image, (350, 40))
        pygame.display.update()
    
    # displays the card and gui settings for when waiting for the opponent
    def waiting_for_player(self, opponent_move ):
        
        self.screen.blit(self.read_card, (350, 410))
        if opponent_move == False:
            self.clear_center_text()
            self.result  = self.font.render("Player is Ready: Waiting for Opponent Move", True, (0, 0, 0))
            self.annoucement = "Player is Ready: Waiting for Opponent Move"
            text_pos = self.result.get_rect(center=(self.width//2, self.height//2))
            self.screen.blit(self.result, text_pos)
        pygame.display.update()

    # displays message to click on your card to play it
    def click_card_instruction(self):
        self.clear_center_text()
        self.output  = self.font.render("Click on your card to play it", True, (0, 0, 0))
        self.annoucement = "Click on your card to play it"
        text_pos = self.output.get_rect(center=(self.width//2, self.height//2))
        self.screen.blit(self.output, text_pos)
        pygame.display.update()
    
    # display results
    def display_result(self, result):
        self.clear_center_text()
        self.output  = self.font.render(f"{result} wins round", True, (0, 0, 0))
        self.annoucement = f"{result} wins round"
        text_pos = self.output.get_rect(center=(self.width//2, self.height//2))
        self.screen.blit(self.output, text_pos)
        pygame.display.update()
    # display when the game ends
    def display_end(self, result):
        self.clear_center_text()
        self.output  = self.font.render(f"{result}", True, (0, 0, 0))
        self.annoucement = f"{result}"
        text_pos = self.output.get_rect(center=(self.width//2, self.height//2))
        self.screen.blit(self.output, text_pos)
        pygame.display.update()
        
    # display when war ends
    def display_war(self):
        self.clear_center_text()
        self.output  = self.font.render("War!", True, (0, 0, 0))
        self.annoucement = "War!"
        text_pos = self.output.get_rect(center=(self.width//2, self.height//2))
        self.screen.blit(self.output, text_pos)
        pygame.display.update()
    # display when there is war
    def display_war_cards(self, war_count):
        war_count = int(war_count) * 8
        card_overlap = 1.9 * war_count
        total_width = (self.card_width - card_overlap) * war_count / 2 + 100

        # Calculate the x-coordinate of the leftmost card
        x = (self.width - total_width) / 2 + 50
        # Display the cards in two rows
        for i in range(war_count//2):
            self.screen.blit(pygame.transform.scale(self.card_back, (100, 140)), (x,  self.height/2 - self.card_height/2 + 30))
            self.screen.blit(pygame.transform.scale(self.card_back, (100, 140)), (x, self.height/2 - self.card_height/2 - 40))
            x += self.card_width - card_overlap
    # clears the text in the middle
    def clear_center_text(self):
        self.output  = self.font.render(self.annoucement, True, (0, 0, 0))
        text_rect = self.output.get_rect(center=(self.width//2, self.height//2))
        pygame.draw.rect(self.screen, (background_green), text_rect)
        pygame.display.update()
    # calculates area for the button press for the card
    def is_within_area(self,coords, area):
        x, y = coords
        area_x, area_y, width, height = area
        return area_x <= x <= area_x + width and area_y <= y <= area_y + height
    # handles close  
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
