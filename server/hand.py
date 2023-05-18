import random
from .card import Card
import json

class Hand:

    def __init__(self):
        self.cards: list[Card] = []
        
    def __str__(self):
        cards_str = [str(card) for card in self.cards]
        return ", ".join(cards_str)
    
    def to_json(self):
        return [card.to_json() for card in self.cards]
    
    def pop(self):
        return self.cards.pop(0)
    
    def push(self, card: Card):
        self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)
        
    def is_empty(self):
        return len(self) == 0

    def clear(self):
        self.cards.clear()

    def __len__(self):
        return len(self.cards)

    def __contains__(self, item):
        return item in self.cards

    def __getitem__(self, key):
        return self.cards[key]
