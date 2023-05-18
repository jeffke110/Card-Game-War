import random
from .card import Card
import json


class Deck:
    def __init__(self):
        self.cards = []
        for suit in ['Spades', 'Hearts', 'Diamonds', 'Clubs']:
            for rank in range(2, 15):
                #self.cards.append(Card(suit, random.randint(2, 4)))
                self.cards.append(Card(suit, rank))
    
    def __str__(self):
        return ", ".join([str(card) for card in self.cards])
    
    def to_json(self):
        return [card.to_json() for card in self.cards]
    
    def is_empty(self):
            return len(self.cards) == 0

    def pop(self):
        return self.cards.pop(0)

    def push(self, card: Card):
        self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def __len__(self):
        return len(self.cards)

    def __contains__(self, item):
        return item in self.cards

    def __add__(self, other):
        if not isinstance(other, Deck):
            raise TypeError("invalid types")

        result = Deck(empty=True)
        result.cards = self.cards + other.cards
        return result


