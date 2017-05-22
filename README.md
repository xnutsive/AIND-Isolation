# Udacity AIND Isolation project implementation

This is a solution for Udacity's AIND Isolation project.
For more details on the project, [read the original readme](https://github.com/xnutsive/AIND-Isolation/blob/master/AIND-SPEC-README.md).

This implementation was forked from Udacity's original repository for April 2017 cohort. The implementation was not tested with later versions of the environment.

### Implemented features
1. Minimax game playing agent.
2. Alphabeta pruning
3. Caching scored boards and searching for an existing score (rotating the board), helps increase depth for the first few moves.

No opening books or MCTS algs implemented.

### Evaluation heuristics

Uses the `improved_heuristic` for now, which is `player_moves - opponent_moves`.

### Structure

No additional libraries are used except for `itertools`. No additional files required to run the code. If you're familiar with the AIND original project, this code should look pretty readable to you. 

`game_agent.py` contains the required techniques and no optional optimisations. 

`agent_test.py` test that `AlphabetaPlayer` and `MinimaxPlayer` can initialize and return valid moves and that's it.

`competition_agent.py` is based on `AlphaBetaPlayer` and contains some improvements (tree pruning, etc).

