import itertools


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
        This heuristic is the count of available next moves for the player. 

    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    return float(max(0, len(own_moves) - len(opp_moves)))


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    uniq_moves = [m for m in own_moves if m not in opp_moves]
    return float(len(own_moves) + len(uniq_moves) - len(opp_moves))


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(max(0, own_moves - 2 * opp_moves))


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

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
            best_move = self.minimax(game, self.search_depth)
        except SearchTimeout:
            pass
        return best_move

    def minimax(self, game, depth):
        """
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        return max(map(lambda m: (m, self.min_play(game.forecast_move(m), depth-1)),
                       game.get_legal_moves(self)),
                   key=lambda x: x[1])[0]

    def min_play(self, game, depth):
        """
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        int
            Score of proposed board when minimizing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()

        if not legal_moves or depth == 0:
            return self.score(game, self)

        return min(map(lambda m: self.max_play(game.forecast_move(m), depth-1), legal_moves))

    def max_play(self, game, depth):
        """
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        int
            Score of proposed board when maximizing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()

        if not legal_moves or depth == 0:
            return self.score(game, self)

        return max(map(lambda m: self.min_play(game.forecast_move(m), depth-1), legal_moves))


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

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
            score = self.min_play(game.forecast_move(move), depth-1, alpha, beta)

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
            value = min(value, self.max_play(game.forecast_move(move), depth-1, alpha, beta))
            if value <= alpha: return value
            beta = min(beta, value)

        return value

    def max_play(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD: raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        value = float("-inf")

        if not legal_moves or depth == 0:
            score = self.score(game, self)

            return self.score(game, self)

        for move in legal_moves:
            value = max(value, self.min_play(game.forecast_move(move), depth-1, alpha, beta))
            if value >= beta: return value
            alpha = max(alpha, value)

        return value
