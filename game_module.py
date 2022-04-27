
# %%


from copy import deepcopy
import random
random.seed(0)

def status_decoder():
    pass


def status_encoder():
    pass

def random_game_status(seed):
    pass

class Move:
    def __init__(self, start_pos=None, end_pos=None, removed_opponent_pos=None, jump_through_pos=[]) -> None:
        # print('removed opponent pos: ', removed_opponent_pos)
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.removed_opponent_pos = removed_opponent_pos
        self.jump_through_pos = jump_through_pos
        self.move_score = 0

class GameBoard:
    _board_size = 8  # default is an 8*8 game
    _init_pos_size = 4  # 4

    def __init__(self, **kwag) -> None:
        self.p1_position = set([(i, j) for i in range(
            0, self._init_pos_size) for j in range(0, self._init_pos_size-i)])
        self.p2_position = set([(self._board_size-1-i, self._board_size-1-j)
                               for i in range(0, self._init_pos_size) for j in range(0, self._init_pos_size-i)])
        self.turn_player = 'player_1'
        if kwag:
            if 'p1_position' in kwag.keys():
                self.p1_position = set(kwag['p1_position'])
            if 'p2_position' in kwag.keys():
                self.p2_position = set(kwag['p2_position'])
            if 'turn_player' in kwag.keys():
                self.turn_player = kwag['turn_player']
        self.valid_move_list = []

    def generate_round_moves(self):
        """
        ::return:: current_position and new_position
        """


        # --------- #
        valid_move_list = []
        current_position = []
        if self.turn_player == 'player_2':
            current_position = self.p2_position
        else:
            current_position = self.p1_position

        for pos in current_position:
            # print('\n\nGENERATE moves for %s' % (str(pos)))
            valid_move_list = valid_move_list + generate_moves(self, start_pos=pos)
        self.valid_move_list = valid_move_list
        # return move_dict

    def evaluation(self):
        pass
    
    def is_winning(self):
        if self.turn_player == 'player_1':
            if (7, 7) in self.p1_position:
                return True
            elif len(self.p2_position) == 1 and len(self.p1_position) > 1:
                return True
        elif self.turn_player == 'player_2':
            if (0, 0) in self.p2_position:
                return True
            elif len(self.p1_position) == 1 and len(self.p2_position) > 1:
                return True
        return False
    
    def is_draw(self):
        if len(self.p1_position) == 1 and len(self.p2_position) == 1:
            return True
        return False

    def list_all_valid_moves(self):
        valid_moves_dict = {}
        for move in self.valid_move_list:
            key_str = '{}->{}'.format(move.start_pos, move.end_pos)
            valid_moves_dict[key_str] = move
        return valid_moves_dict

class HumanPlayer:
    def __init__(self, player=1) -> None:
        if player == 1: 
            self.turn_player = 'player_1'
        elif player == 2: 
            self.turn_player = 'player_2'
        else:
            raise Exception('The player should be: 1 or 2.')
    
    def choose_a_move(self, board:GameBoard) -> Move:
        valid_moves_dict = board.list_all_valid_moves()
        print([x for x in valid_moves_dict.keys()])
        chosen_key = str(input('Input the move option'))
        return valid_moves_dict[chosen_key] # move

class RandomPlayer:
    def __init__(self, player=1) -> None:
        if player == 1: 
            self.turn_player = 'player_1'
        elif player == 2: 
            self.turn_player = 'player_2'
        else:
            raise Exception('The player should be: 1 or 2.')

    def choose_a_move(self, board:GameBoard) -> Move:
        random_index = random.randint(0, len(board.valid_move_list)-1)
        return board.valid_move_list[random_index] # move

class SmartPlayer:
    def __init__(self) -> None:
        pass

### ---------------------------------------- ###
# Functions for playing the game
def is_valid(status: GameBoard, start_pos: tuple, move: tuple, last_pos: tuple = None, jump_through: tuple = None, previous_steps: Move = None):
    # if move is out of border
    if move[0] >= status._board_size or move[1] >= status._board_size or move[0] < 0 or move[1] < 0:
        return False

    # if the move pos is occupied (included intermediate points and end points)
    if move in status.p1_position or move in status.p2_position:
        return False

    # Prevent jumping back to the start pos
    if last_pos:
        if move == last_pos:
            return False

    # Prevent jumping into back patterns
    if jump_through and previous_steps:
        # print('jump_through', jump_through, 'previous_steps.jump_through_pos:', previous_steps.jump_through_pos)
        if jump_through in previous_steps.jump_through_pos:
            return False

    return True

def generate_moves(status: GameBoard, start_pos: tuple,
                    previous_steps: Move = None, is_jumping: bool = False, 
                    last_pos: tuple=None, has_remove: bool = False):
    """
    start_pos: the original position the piece stands
    previous_steps: a valid move
    """
    # print('\nstart pos:', start_pos)
    # if previous_steps:
    #     print('the original start: ', previous_steps.start_pos)

    valid_moves = []
    # status 1: a initial start (when start jumping, we cannot use the normal move method)
    if not is_jumping:
        # normal move
        # --- for player 1: only can move downward or right
        if status.turn_player == 'player_1':
            move_set = [(start_pos[0]+1, start_pos[1]), (start_pos[0],
                                                            start_pos[1]+1), (start_pos[0]+1, start_pos[1]+1)]

        # --- for player 2: only can move upward or left
        elif status.turn_player == 'player_2':
            move_set = [(start_pos[0]-1, start_pos[1]), (start_pos[0],
                                                            start_pos[1]-1), (start_pos[0]-1, start_pos[1]-1)]
        for move_pos in move_set:
            if is_valid(status, start_pos, move_pos):
                # valid_moves = valid_moves + [move_pos]
                move = Move(start_pos, move_pos)
                valid_moves = valid_moves + [move]

    # status 1 & 2: a initial start
    # jumping moves (start jumping): 8 possible directions
    neighbor_set = [(start_pos[0]-1, start_pos[1]), (start_pos[0], start_pos[1]+1), (start_pos[0]-1, start_pos[1]+1), (start_pos[0]+1, start_pos[1]+1),
                    (start_pos[0]+1, start_pos[1]), (start_pos[0], start_pos[1]-1), (start_pos[0]+1, start_pos[1]-1), (start_pos[0]-1, start_pos[1]-1)]
    for neighbor in neighbor_set:
        # Start a jump
        if neighbor in status.p1_position or neighbor in status.p2_position:
            diff = (neighbor[0]-start_pos[0],
                    neighbor[1]-start_pos[1])
            # Next position -- jump cross the neighbor
            move_pos = (neighbor[0]+diff[0], neighbor[1]+diff[1])
            # print('try the neighbor:', neighbor, diff, 'jump moves: ', move_pos)

            if is_valid(status, start_pos, move_pos, last_pos=last_pos, 
                        jump_through=neighbor, previous_steps=previous_steps):
                # print('is a valid jump:', move_pos, 'the last pos:', last_pos)
                
                # Prepare for keep jumping
                new_status = deepcopy(status)
                remove_pos = None
                if status.turn_player == 'player_1':
                    new_status.p1_position.remove(start_pos)
                    new_status.p1_position.add(move_pos)
                    if (not has_remove) and neighbor in new_status.p2_position:
                        remove_pos = neighbor
                        # print('a remove:', remove_pos)
                        new_status.p2_position.remove(remove_pos)
                        has_remove = True

                elif status.turn_player == 'player_2':
                    new_status.p2_position.remove(start_pos)
                    new_status.p2_position.add(move_pos)
                    if (not has_remove) and neighbor in new_status.p1_position:
                        remove_pos = neighbor
                        new_status.p1_position.remove(remove_pos)
                        has_remove = True

                # Add the option to the result set
                if not previous_steps:
                    move = Move(start_pos, move_pos, 
                        removed_opponent_pos=remove_pos, jump_through_pos=[neighbor])
                    valid_moves = valid_moves + [move]
                else:
                    jump_through_pos = previous_steps.jump_through_pos + [neighbor]
                    move = Move(previous_steps.start_pos, move_pos, 
                        removed_opponent_pos=remove_pos, jump_through_pos=jump_through_pos)
                    valid_moves = valid_moves + [move]

                # Try to keep jumping: Create a new game status for making the move:
                new_start_pos = move_pos

                valid_jump_moves = generate_moves(
                    new_status, new_start_pos, previous_steps=move, is_jumping=True, 
                    last_pos=start_pos, has_remove=has_remove)
                valid_moves = valid_moves + valid_jump_moves

    return valid_moves

def make_a_move(board:GameBoard, move:Move):
    new_board = deepcopy(board)
    if new_board.turn_player == 'player_1':
        new_board.p1_position.remove(move.start_pos)
        new_board.p1_position.add(move.end_pos)
        new_board.turn_player = 'player_2'
        if move.removed_opponent_pos:
            new_board.p2_position.remove(move.removed_opponent_pos)
    elif new_board.turn_player == 'player_2':
        new_board.p2_position.remove(move.start_pos)
        new_board.p2_position.add(move.end_pos)
        new_board.turn_player = 'player_1'
        if move.removed_opponent_pos:
            new_board.p1_position.remove(move.removed_opponent_pos)
    return new_board

#%%
# ### ---------------------------------------- ###
# start a game
game = GameBoard()
player_1 = RandomPlayer(player=1)
player_2 = RandomPlayer(player=2)
round = 0
while True:
    game.generate_round_moves()
    if game.turn_player == 'player_1':
        move = player_1.choose_a_move(game)
    elif game.turn_player == 'player_2':
        move = player_2.choose_a_move(game)

    game = make_a_move(game, move)
    round += 1
    print('Round: %s\nP1: %s\nP2: %s' % (round, game.p1_position, game.p2_position))

    if game.is_draw() or game.is_winning():
        break

print('The Winner:', game.turn_player, '; Total rounds of the game:', round)

#%%
### ---------------------------------------- ###
# a = GameBoard()
# a.generate_round_moves()

ini_pos_1 = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0),
             (1, 1), (1, 2), (2, 0), (2, 1), (3, 0)]
ini_pos_2 = [(7, 7), (7, 6), (7, 5), (7, 4), (6, 7),
             (6, 6), (6, 5), (5, 7), (5, 6), (4, 7)]
a = GameBoard(p1_position=ini_pos_1, p2_position=ini_pos_2, turn_player = 'player_2')

a = GameBoard()
a.generate_round_moves()
a.list_all_valid_moves()
# move_dict = a.generate_round_moves()

#%%
try_pos_1 = [(2, 0), (3, 2), (3, 1)]
try_pos_2 = [(4, 3), (4, 5)]

a = GameBoard(p1_position=try_pos_1, p2_position=try_pos_2, turn_player = 'player_2')
a.generate_round_moves()
a.list_all_valid_moves()
# move_dict = a.generate_round_moves()

# move_dict[(3,1)][3] --> this is a move
# move_dict[(3,1)][3].start_pos


# %%

random.seed(0)

# %%
try_pos_1 = [(2, 0)]
# try_pos_2 = [(4, 3), (4, 5), (1, 0)]
try_pos_2 = [(4, 3)]
try_pos_1 = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0),
             (1, 1), (1, 2), (2, 0), (2, 1), (3, 0)]
try_pos_2 = [(7, 7), (7, 6), (7, 5), (7, 4), (6, 7),
             (6, 6), (6, 5), (5, 7), (5, 6), (4, 7)]
game = GameBoard(p1_position=try_pos_1, p2_position=try_pos_2, turn_player = 'player_1')