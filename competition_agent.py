import random
import itertools

from isolation import Board
from game_agent import AlphaBetaPlayer
from sample_players import improved_score


class SearchTimeout(Exception):
    pass


def custom_score(game, player):
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    return float(len(own_moves) - len(opp_moves))


def get_board_clockwise_rotation(game):
    rotated = game.copy()

    for j in range(game.height):
        for i in range(game.height):
            rotated._board_state[(game.height-1-j) + i*game.height] = \
                game._board_state[j*game.height + i]

    return rotated


class CustomPlayer:
    """Game-playing agent to use in the optional player vs player Isolation
    competition.

    You must at least implement the get_move() method and a search function
    to complete this class, but you may use any of the techniques discussed
    in lecture or elsewhere on the web -- opening books, MCTS, etc.

    **************************************************************************
          THIS CLASS IS OPTIONAL -- IT IS ONLY USED IN THE ISOLATION PvP
        COMPETITION.  IT IS NOT REQUIRED FOR THE ISOLATION PROJECT REVIEW.
    **************************************************************************

    Parameters
    ----------
    data : string
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted.  Note that
        the PvP competition uses more accurate timers that are not cross-
        platform compatible, so a limit of 1ms (vs 10ms for the other classes)
        is generally sufficient.
    """

    def __init__(self, data=None, timeout=1.):
        self.score = custom_score
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
        self.saved_games = dict()
        self.reached_nodes = 0

    def get_move(self, game, time_left):
        self.time_left = time_left
        best_move = (-1, -1)

        reached_depth = 0

        try:
            for depth in itertools.count(1):
                best_move = self.alphabeta(game, depth, float("-inf"), float("inf"))
                reached_depth = depth  # save deepest search attempt that succeeded

                # print("Move: " + str(game.move_count) + ", depth: " + str(reached_depth) +
                #      ", saved states " + str(len(self.saved_games)) + ", nodes: " + str(self.reached_nodes))
        except SearchTimeout:
            pass

        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        if self.time_left() < self.TIMER_THRESHOLD: raise SearchTimeout()

        legal_moves = game.get_legal_moves(self)
        best_move = legal_moves[0] if legal_moves else (-1, -1)
        best_score = float("-inf")

        self.saved_games = dict()  # delete the old search scores
        self.reached_nodes = 0

        for move in legal_moves:
            score = self.min_play(game.forecast_move(move), depth - 1, alpha, beta)

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, best_score)

        return best_move

    def min_play(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD: raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        value = float("inf")

        if not legal_moves or depth == 0:
            # Check if we have this board's score handy and return if we do
            if game.hash() in self.saved_games: return self.saved_games[game.hash()]

            # Approximate the score
            score = self.score(game, self)

            # Save the calculated score for all the rotated boards

            self.saved_games[game.hash()] = score
            self.reached_nodes += 1
            rotated = game
            for i in range(3):
                rotated = get_board_clockwise_rotation(rotated)
                self.saved_games[rotated.hash()] = score

            return score

        for move in legal_moves:
            value = min(value, self.max_play(game.forecast_move(move), depth - 1, alpha, beta))
            if value <= alpha: return value
            beta = min(beta, value)

        return value

    def max_play(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD: raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        value = float("-inf")

        if not legal_moves or depth == 0:

            # Check if we have this board's score handy and return if we do
            if game.hash() in self.saved_games: return self.saved_games[game.hash()]

            # Approximate the score
            score = self.score(game, self)

            # Save the calculated score for all the rotated boards

            self.saved_games[game.hash()] = score
            self.reached_nodes += 1
            rotated = game
            for i in range(3):
                rotated = get_board_clockwise_rotation(rotated)
                self.saved_games[rotated.hash()] = score

            return score

        for move in legal_moves:
            value = max(value, self.min_play(game.forecast_move(move), depth - 1, alpha, beta))
            if value >= beta: return value
            alpha = max(alpha, value)

        return value


if __name__ == '__main__':
    print("Custom vs Alphabeta")

    for i in range(10):
        alphabeta = AlphaBetaPlayer(score_fn=improved_score)
        custom = CustomPlayer()

        board = Board(alphabeta, custom)
        print(board.play(time_limit=1000)[0])
