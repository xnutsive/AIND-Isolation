"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest
import timeit
import random
from importlib import reload

from isolation import Board
from game_agent import AlphaBetaPlayer, MinimaxPlayer,\
    custom_score, custom_score_2, custom_score_3
from sample_players import RandomPlayer, GreedyPlayer, \
    open_move_score, improved_score, center_score


class IsolationTest(unittest.TestCase):

    def setUp(self):
        self.time_millis = lambda: 1000 * timeit.default_timer()

    def test_minimax_valid(self):
        test_start = self.time_millis()
        time_left = lambda: 1000 - (self.time_millis() - test_start)

        minimax = MinimaxPlayer()
        board = Board(minimax, RandomPlayer())

        # Play two moves to make legal moves array much smaller
        board.apply_move(random.choice(board.get_legal_moves()))
        board.apply_move(random.choice(board.get_legal_moves()))

        self.assertIn(minimax.get_move(board, time_left),
                      board.get_legal_moves(minimax))

    def test_alphabeta_valid(self):
        test_start = self.time_millis()
        time_left = lambda: 1000 - (self.time_millis() - test_start)

        alphabeta = MinimaxPlayer()
        board = Board(alphabeta, RandomPlayer())

        # Play two moves to make legal moves array much smaller
        board.apply_move(random.choice(board.get_legal_moves()))
        board.apply_move(random.choice(board.get_legal_moves()))

        self.assertIn(alphabeta.get_move(board, time_left),
                      board.get_legal_moves(alphabeta))


if __name__ == '__main__':
    unittest.main()
