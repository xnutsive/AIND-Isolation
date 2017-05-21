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

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        best_move = (-1, -1)

        try:
            for depth in itertools.count(1):
                best_move = self.alphabeta(game, depth, float("-inf"), float("inf"))
        except SearchTimeout:
            pass

        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """
        Searches for the best move using minimax and alphabeta pruning with 
        iterative deepening until the depth provided in the args.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD: raise SearchTimeout()

        legal_moves = game.get_legal_moves(self)
        best_move = legal_moves[0] if legal_moves else (-1, -1)
        best_score = float("-inf")

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
            return self.score(game, self)

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
            return self.score(game, self)

        for move in legal_moves:
            value = max(value, self.min_play(game.forecast_move(move), depth - 1, alpha, beta))
            if value >= beta: return value
            alpha = max(alpha, value)

        return value


if __name__ == '__main__':
    print("Custom vs Alphabeta")

    alphabeta = AlphaBetaPlayer(score_fn=improved_score)
    custom = CustomPlayer()

    board = Board(alphabeta, custom)
    print(board.play(time_limit=1000))
