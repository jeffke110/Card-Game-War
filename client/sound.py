import pygame

class Sound:
    def __init__(self):
        pygame.mixer.init()
        self.card_flip = pygame.mixer.Sound("sounds/cardflip.wav")
        self.win = pygame.mixer.Sound("sounds/win.wav")
        self.lose = pygame.mixer.Sound("sounds/lose.wav")
        self.war = pygame.mixer.Sound("sounds/war.wav")
        
    def player_flip(self):
        self.card_flip.play()
        while pygame.mixer.get_busy():
            pygame.time.wait(100)
            
    def play_win(self):
        self.win.play()
        while pygame.mixer.get_busy():
            pygame.time.wait(100)
    
    def play_lose(self):
        self.lose.play()
        while pygame.mixer.get_busy():
            pygame.time.wait(100)
            
    def play_war(self):
        self.war.play()
        while pygame.mixer.get_busy():
            pygame.time.wait(100)


   