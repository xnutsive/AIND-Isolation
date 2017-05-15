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
        self.minimax_player = game_agent.MinimaxPlayer()
        self.alphabeta_player = game_agent.AlphaBetaPlayer()
        self.random_player = sample_players.RandomPlayer()

        self.game = isolation.Board(self.minimax_player, self.random_player)
        self.alphabeta_game = isolation.Board(self.alphabeta_player, self.random_player)

        self.time_millis = lambda: 1000 * timeit.default_timer()

    def test_gives_valid_move(self):
        test_start = self.time_millis()

        # limit - miliseconds from start
        time_left = lambda: 10000 - (self.time_millis() - test_start)

        self.assertIn(self.minimax_player.get_move(self.game, time_left),
                      self.game.get_legal_moves(self.minimax_player))

    def test_alphabeta_valid(self):
        test_start = self.time_millis()

        # limit - miliseconds from start
        time_left = lambda: 10000 - (self.time_millis() - test_start)

        self.assertIn(self.alphabeta_player.get_move(self.alphabeta_game, time_left),
                      self.alphabeta_game.get_legal_moves(self.alphabeta_player))


if __name__ == '__main__':
    unittest.main()
