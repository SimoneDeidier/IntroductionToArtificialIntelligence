from copy import deepcopy
import math

State = tuple[int, list[list[int | None]]]  # Tuple of player (whose turn it is), and board
Action = tuple[int, int]  # Where to place the player's piece

class Game:
    
    def initial_state(self) -> State:
        return (0, [[None, None, None], [None, None, None], [None, None, None]])

    def to_move(self, state: State) -> int:
        player_index, _ = state
        return player_index

    def actions(self, state: State) -> list[Action]:
        _, board = state
        actions = []
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    actions.append((row, col))
        return actions

    def result(self, state: State, action: Action) -> State:
        _, board = state
        row, col = action
        next_board = deepcopy(board)
        next_board[row][col] = self.to_move(state)
        return (self.to_move(state) + 1) % 2, next_board

    def is_winner(self, state: State, player: int) -> bool:
        _, board = state
        for row in range(3):
            if all(board[row][col] == player for col in range(3)):
                return True
        for col in range(3):
            if all(board[row][col] == player for row in range(3)):
                return True
        if all(board[i][i] == player for i in range(3)):
            return True
        return all(board[i][2 - i] == player for i in range(3))

    def is_terminal(self, state: State) -> bool:
        _, board = state
        if self.is_winner(state, (self.to_move(state) + 1) % 2):
            return True
        return all(board[row][col] is not None for row in range(3) for col in range(3))

    def utility(self, state, player):
        assert self.is_terminal(state)
        if self.is_winner(state, player):
            return 1
        if self.is_winner(state, (player + 1) % 2):
            return -1
        return 0

    def print(self, state: State):
        _, board = state
        print()
        for row in range(3):
            cells = [
                ' ' if board[row][col] is None else 'x' if board[row][col] == 0 else 'o'
                for col in range(3)
            ]
            print(f' {cells[0]} | {cells[1]} | {cells[2]}')
            if row < 2:
                print('---+---+---')
        print()
        if self.is_terminal(state):
            if self.utility(state, 0) > 0:
                print(f'P1 won')
            elif self.utility(state, 1) > 0:
                print(f'P2 won')
            else:
                print('The game is a draw')
        else:
            print(f'It is P{self.to_move(state)+1}\'s turn to move')

def alpha_beta_search(game: Game, state: State) -> Action | None:
    
    player = game.to_move(state)  # Determine which player is to move

    def max_value(state: State, alpha: float, beta: float) -> float:
        if game.is_terminal(state):  # Check if the game is over
            return game.utility(state, player)  # Return the utility value of the terminal state
        v = -math.inf
        for action in game.actions(state):  # Iterate over all possible actions
            v = max(v, min_value(game.result(state, action), alpha, beta))  # Get the maximum value
            if v >= beta:  # Beta cutoff
                return v
            alpha = max(alpha, v)  # Update alpha
        return v

    def min_value(state: State, alpha: float, beta: float) -> float:
        if game.is_terminal(state):  # Check if the game is over
            return game.utility(state, player)  # Return the utility value of the terminal state
        v = math.inf
        for action in game.actions(state):  # Iterate over all possible actions
            v = min(v, max_value(game.result(state, action), alpha, beta))  # Get the minimum value
            if v <= alpha:  # Alpha cutoff
                return v
            beta = min(beta, v)  # Update beta
        return v

    best_score = -math.inf
    best_action = None
    alpha = -math.inf
    beta = math.inf
    for action in game.actions(state):  # Iterate over all possible actions
        value = min_value(game.result(state, action), alpha, beta)  # Get the value of the action
        if value > best_score:  # Check if this action has the best score
            best_score = value
            best_action = action
        alpha = max(alpha, best_score)  # Update alpha
    return best_action  # Return the best action



game = Game()

state = game.initial_state()
game.print(state)
while not game.is_terminal(state):
    player = game.to_move(state)
    action = alpha_beta_search(game, state) # The player whose turn it is, is the MAX player
    print(f'P{player + 1}\'s action : { action }')
    assert action is not None
    state = game.result(state, action)
    game.print(state)