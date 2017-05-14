"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent
import sample_players
import timeit

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = game_agent.MinimaxPlayer()
        self.player2 = sample_players.RandomPlayer()
        self.game = isolation.Board(self.player1, self.player2)
        self.time_millis = lambda: 1000 * timeit.default_timer()


    def test_gives_valid_move(self):
        test_start = self.time_millis()

        # limit - miliseconds from start
        time_left = lambda: 10000 - (self.time_millis() - test_start)

        self.assertIn(self.player1.get_move(self.game, time_left),
                      self.game.get_legal_moves(self.player1))


    def test_visits_levels(self):
        self.fail("Mot Implemented")

    def test_visits_nodes(self):
        self.fail("Not implemented")


if __name__ == '__main__':
    unittest.main()
