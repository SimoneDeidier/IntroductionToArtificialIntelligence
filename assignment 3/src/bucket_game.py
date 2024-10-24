import math

State = tuple [int, list[str | int]] # Tuple of player ( whose turn it is ) , and the buckets ( as str ) or the number in a bucket
Action = str | int # Bucket choice ( as str ) or choice of number

class Game:
    
    def initial_state(self) -> State:
        return 0, ['A', 'B', 'C']
    
    def to_move(self, state : State) -> int:
        player , _ = state
        return player
    
    def actions(self, state : State) -> list[Action]:
        _ , actions = state
        return actions
    
    def result(self, state : State, action : Action) -> State: 
        if action == 'A':
            return (self.to_move(state) + 1) % 2, [-50 , 50]
        elif action == 'B':
            return (self.to_move(state) + 1) % 2, [3 , 1]
        elif action == 'C':
            return (self.to_move(state) + 1) % 2, [-5 , 15]
        assert type(action) is int
        return (self.to_move(state) + 1) % 2, [action]
    
    def is_terminal(self, state : State) -> bool:
        _ , actions = state 
        return len(actions) == 1
    
    def utility(self, state : State, player : int) -> float:
        assert self.is_terminal(state)
        _ , actions = state
        assert type(actions[0]) is int
        return actions[0] if player == self.to_move(state) else -actions[0]
    
    def print(self , state):
        print(f'The state is {state} and ', end = '')
        if self.is_terminal(state):
            print (f'P1\'s utility is {self.utility(state , 0)}')
        else :
            print (f'it is P{self.to_move(state) + 1}\'s turn')

def minimax_search(game: Game, state: State) -> Action | None:
    
    player = game.to_move(state)

    def max_value(state: State) -> float:
        # If the state is terminal, return the utility value for the player
        if game.is_terminal(state):
            return game.utility(state, player)
        v = -math.inf
        # Iterate over all possible actions and choose the one with the maximum value
        for action in game.actions(state):
            v = max(v, min_value(game.result(state, action)))
        return v

    def min_value(state: State) -> float:
        # If the state is terminal, return the utility value for the player
        if game.is_terminal(state):
            return game.utility(state, player)
        v = math.inf
        # Iterate over all possible actions and choose the one with the minimum value
        for action in game.actions(state):
            v = min(v, max_value(game.result(state, action)))
        return v

    best_score = -math.inf
    best_action = None
    # Evaluate all possible actions and choose the one with the best score
    for action in game.actions(state):
        value = min_value(game.result(state, action))
        if value > best_score:
            best_score = value
            best_action = action
    return best_action



game = Game()

state = game.initial_state()
game.print(state)
while not game.is_terminal(state):
    player = game.to_move(state)
    action = minimax_search(game, state) # The player whose turn it is, is the MAX player
    print(f'P{player + 1}\'s action : { action }')
    assert action is not None
    state = game.result(state, action)
    game.print(state)