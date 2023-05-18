import unittest
from unittest.mock import Mock

from server.publisher import MyPublisher, Player

class TestMyPublisher(unittest.TestCase):
    def setUp(self):
        self.publisher = MyPublisher()

    def test_add_subscriber(self):
        player1 = Player(Mock())
        player2 = Player(Mock())
        self.publisher.add_subscriber(player1)
        self.assertEqual(len(self.publisher._subscribers), 1)
        self.assertIn(player1, self.publisher._subscribers)
        print("Player 1 subscribed successfully")
        self.publisher.add_subscriber(player2)
        self.assertEqual(len(self.publisher._subscribers), 2)
        self.assertIn(player2, self.publisher._subscribers)
        print("Player 2 subscribed successfully")

    def test_remove_subscriber(self):
        player1 = Player(Mock())
        player2 = Player(Mock())
        self.publisher.add_subscriber(player1)
        self.publisher.add_subscriber(player2)
        self.publisher.remove_subscriber(player1)
        self.assertEqual(len(self.publisher._subscribers), 1)
        self.assertNotIn(player1, self.publisher._subscribers)
        self.assertIn(player2, self.publisher._subscribers)
        print("Player 1 removed successfully")
        self.publisher.remove_subscriber(player2)
        self.assertEqual(len(self.publisher._subscribers), 0)
        self.assertNotIn(player1, self.publisher._subscribers)
        self.assertNotIn(player2, self.publisher._subscribers)
        print("Player 2 removed successfully")