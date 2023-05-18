import pytest
from server.hand import Hand
from server.card import Card

def test_hand_creation():
    hand = Hand()
    assert len(hand) == 0

def test_push_card():
    hand = Hand()
    card = Card("spades", 10)
    hand.push(card)
    assert len(hand) == 1
    assert card in hand

def test_pop_card():
    hand = Hand()
    card = Card("hearts", 7)
    hand.push(card)
    assert len(hand) == 1
    popped_card = hand.pop()
    assert len(hand) == 0
    assert popped_card == card

def test_shuffle():
    hand = Hand()
    cards = [Card("hearts", 7), Card("clubs", 4), Card("diamonds", 2)]
    for card in cards:
        hand.push(card)
    assert len(hand) == 3
    original_order = str(hand)
    hand.shuffle()
    shuffled_order = str(hand)
    assert len(hand) == 3
    assert original_order != shuffled_order

def test_is_empty():
    hand = Hand()
    assert hand.is_empty()
    hand.push(Card("diamonds", 8))
    assert not hand.is_empty()

def test_clear():
    hand = Hand()
    hand.push(Card("spades", 5))
    hand.push(Card("hearts", 9))
    assert len(hand) == 2
    hand.clear()
    assert len(hand) == 0
    
def test_contains():
    hand = Hand()
    card = Card("spades", 2)
    assert card not in hand
    hand.push(card)
    assert card in hand

def test_getitem():
    hand = Hand()
    cards = [Card("spades", 2), Card("hearts", 7), Card("clubs", "K")]
    for card in cards:
        hand.push(card)
    assert hand[0] == cards[0]
    assert hand[1] == cards[1]
    assert hand[2] == cards[2]

def test_str():
    hand = Hand()
    hand.push(Card("hearts", 9))
    hand.push(Card("diamonds", 4))
    assert str(hand) == "9 of hearts, 4 of diamonds"