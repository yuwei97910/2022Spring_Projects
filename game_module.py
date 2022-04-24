
# %%


from copy import deepcopy
import random


def status_decoder():
    pass


def status_encoder():
    pass


def random_game_status(seed):
    pass


# %%
class Move:
    def __init__(self) -> None:
        self.start_pos = None
        self.end_pos = None
        self.move_score = 0
        self.move_remove_opponent_pos = None
        self.jump_through_pos = None


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

    def generate_round_moves(self):
        """
        ::return:: current_position and new_position
        """
        def generate_moves(status: GameBoard, start_pos: tuple, jumping_cnt: int = 0, 
                is_jumping: bool = False, last_pos: tuple=None, has_remove: bool = False):
            print('\nstart pos:', start_pos)
            valid_moves = []
            # status 1: a initial start
            if not is_jumping:
                # normal move
                # --- for player 1: only can move downward or right
                if self.turn_player == 'player_1':
                    move_set = [(start_pos[0]+1, start_pos[1]), (start_pos[0],
                                                                 start_pos[1]+1), (start_pos[0]+1, start_pos[1]+1)]

                    for move in move_set:
                        if is_valid(status, start_pos, move):
                            # move = Move()
                            valid_moves = valid_moves + [move]

                # --- for player 2: only can move upward or left
                elif self.turn_player == 'player_2':
                    move_set = [(start_pos[0]-1, start_pos[1]), (start_pos[0],
                                                                 start_pos[1]-1), (start_pos[0]-1, start_pos[1]-1)]
                    for move in move_set:
                        if is_valid(status, start_pos, move):
                            valid_moves = valid_moves + [move]

                # jumping move (start jumping): 8 possible directions
                neighbor_set = [(start_pos[0]-1, start_pos[1]), (start_pos[0], start_pos[1]+1), (start_pos[0]-1, start_pos[1]+1), (start_pos[0]+1, start_pos[1]+1),
                                (start_pos[0]+1, start_pos[1]), (start_pos[0], start_pos[1]-1), (start_pos[0]+1, start_pos[1]-1), (start_pos[0]-1, start_pos[1]-1)]
                for neighbor in neighbor_set:
                    # start a jump
                    if neighbor in status.p1_position or neighbor in status.p2_position:
                        diff = (neighbor[0]-start_pos[0],
                                neighbor[1]-start_pos[1])
                        # next position
                        move = (neighbor[0]+diff[0], neighbor[1]+diff[1])
                        print(neighbor, diff, 'jump moves: ', move)

                        if is_valid(status, start_pos, move):
                            print('is a valid jump:', move)
                            valid_moves = valid_moves + [move]
                            jumping_cnt += 1

                            # Try to keep jumping: Create a new game status for making the move:
                            new_status = deepcopy(status)

                            if self.turn_player == 'player_1':
                                new_status.p1_position.remove(start_pos)
                                new_status.p1_position.add(move)
                                if not has_remove and neighbor in new_status.p2_position:
                                    new_status.p2_position.remove(neighbor)
                                    has_remove = True
                            elif self.turn_player == 'player_2':
                                new_status.p2_position.remove(start_pos)
                                new_status.p2_position.add(move)
                                if not has_remove and neighbor in new_status.p1_position:
                                    new_status.p1_position.remove(neighbor)
                                    has_remove = True
                            new_start_pos = move

                            valid_jump_moves = generate_moves(
                                new_status, new_start_pos, jumping_cnt, is_jumping=True, 
                                last_pos=start_pos, has_remove=has_remove)
                            valid_moves = valid_moves + valid_jump_moves

            # status 2: keep jumping
            elif is_jumping:
                print('--- Keep Jumping: cnt=', jumping_cnt)
                neighbor_set = [(start_pos[0]-1, start_pos[1]), (start_pos[0], start_pos[1]+1), (start_pos[0]-1, start_pos[1]+1), (start_pos[0]+1, start_pos[1]+1),
                                (start_pos[0]+1, start_pos[1]), (start_pos[0], start_pos[1]-1), (start_pos[0]+1, start_pos[1]-1), (start_pos[0]-1, start_pos[1]-1)]
                for neighbor in neighbor_set:
                    if neighbor in status.p1_position or neighbor in status.p2_position:
                        diff = (neighbor[0]-start_pos[0],
                                neighbor[1]-start_pos[1])
                        # next position
                        move = (neighbor[0]+diff[0], neighbor[1]+diff[1])

                        # Prevent jumping back to the start pos
                        if move == last_pos:
                            continue

                        print(neighbor, diff, 'jump moves: ', move)

                        if is_valid(status, start_pos, move):
                            print('is a valid jump:', move)
                            valid_moves = valid_moves + [move]
                            jumping_cnt += 1

                            # Try to keep jumping: Create a new game status for making the move:
                            new_status = deepcopy(status)
                            if self.turn_player == 'player_1':
                                new_status.p1_position.remove(start_pos)
                                new_status.p1_position.add(move)
                                if not has_remove and neighbor in new_status.p2_position:
                                    new_status.p2_position.remove(neighbor)
                                    has_remove = True
                            elif self.turn_player == 'player_2':
                                new_status.p2_position.remove(start_pos)
                                new_status.p2_position.add(move)
                                if not has_remove and neighbor in new_status.p1_position:
                                    new_status.p1_position.remove(neighbor)
                                    has_remove = True
                            new_start_pos = move

                            valid_jump_moves = generate_moves(
                                new_status, new_start_pos, jumping_cnt, is_jumping=True, 
                                last_pos=start_pos, has_remove=has_remove)
                            valid_moves = valid_moves + valid_jump_moves

            return valid_moves

        move_dict = {}
        current_position = []
        if self.turn_player == 'player_2':
            current_position = self.p2_position
        else:
            current_position = self.p1_position

        for pos in current_position:
            move_dict[pos] = generate_moves(self, start_pos=pos)

        return move_dict

    def evaluation(self):
        pass
    
    def is_winning(self):
        pass

class SmartPlayer:
    def __init__(self) -> None:
        pass

### ---------------------------------------- ###
# Functions for playing the game
def is_valid(status: GameBoard, start_pos: tuple, move: tuple):
    # if move is out of border
    if move[0] >= status._board_size or move[1] >= status._board_size or move[0] < 0 or move[1] < 0:
        return False

    # if the move pos is occupied (included intermediate points and end points)
    if move in status.p1_position or move in status.p2_position:
        return False

    return True

def make_a_move(board:GameBoard, move:Move):
    new_board = deepcopy(board)


### ---------------------------------------- ###
# start a game
game = GameBoard()


### ---------------------------------------- ###

# a = GameBoard()
# a.generate_round_moves()

ini_pos_1 = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0),
             (1, 1), (1, 2), (2, 0), (2, 1), (3, 0)]
ini_pos_2 = [(7, 7), (7, 6), (7, 5), (7, 4), (6, 7),
             (6, 6), (6, 5), (5, 7), (5, 6), (4, 7)]

try_pos_1 = [(2, 0), (3, 2), (3, 1)]
try_pos_2 = [(4, 3), (4, 5)]

a = GameBoard(p1_position=try_pos_1, p2_position=try_pos_2)
a.generate_round_moves()
# %%

random.seed(0)

# %%
