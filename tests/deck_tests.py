import unittest
from unittest.mock import patch

from server.card import Card
from server.deck import Deck


class TestDeck(unittest.TestCase):
    def test_init(self):
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)

    def test_is_empty(self):
        deck = Deck()
        self.assertFalse(deck.is_empty())
        for _ in range(52):
            deck.pop()
        self.assertTrue(deck.is_empty())

    def test_pop(self):
        deck = Deck()
        card = deck.pop()
        self.assertIsInstance(card, Card)
        self.assertEqual(len(deck.cards), 51)

    def test_push(self):
        deck = Deck()
        card = Card('Spades', 2)
        deck.push(card)
        self.assertIn(card, deck.cards)

    def test_shuffle(self):
        deck = Deck()
        original_order = str(deck)
        deck.shuffle()
        shuffled_order = str(deck)
        self.assertNotEqual(original_order, shuffled_order)

    def test_len(self):
        deck = Deck()
        self.assertEqual(len(deck), 52)

 

