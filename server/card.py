import json

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
    def to_json(self):
        return {"suit": self.suit, "rank": self.rank}

