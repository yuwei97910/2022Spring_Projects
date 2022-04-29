
# %%

from copy import deepcopy
import random
# random.seed(0)

### ---------------------------------------- ###


def status_decoder():
    pass


def status_encoder():
    pass


### ---------------------------------------- ###


class Move:
    def __init__(self, start_pos=None, end_pos=None, removed_opponent_pos=None, jump_through_pos=[]) -> None:
        # print('removed opponent pos: ', removed_opponent_pos)
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.removed_opponent_pos = removed_opponent_pos
        self.jump_through_pos = jump_through_pos
        # self.move_score = 0


### ---------------------------------------- ###
class GameBoard:
    _board_size = 6  # default is an 8*8 game
    _init_pos_size = 3  # 4

    def __init__(self, **kwag) -> None:
        self.p1_position = set([(i, j)
                                for i in range(0, self._init_pos_size) for j in range(0, self._init_pos_size-i)])
        self.p2_position = set([(self._board_size-1-i, self._board_size-1-j)
                                for i in range(0, self._init_pos_size) for j in range(0, self._init_pos_size-i)])
        self.turn_player = 'player_1'
        self.valid_move_list = []

        # Pre-assigned values
        if kwag:
            if 'p1_position' in kwag.keys():
                self.p1_position = set(kwag['p1_position'])
            if 'p2_position' in kwag.keys():
                self.p2_position = set(kwag['p2_position'])
            if 'turn_player' in kwag.keys():
                self.turn_player = kwag['turn_player']

        # For evaluations
        self.board_score_depth = 0
        self.board_score = 0
        self.opponent_score = 0

    def encoder(self) -> str:
        # all_pos = [(i, j) for i in range(0, self._board_size)
        #               for j in range(0, self._board_size)]

        key = ''  # a key to represent a board would be a string in length 1 + 128
        if self.turn_player == 'player_1':
            key = key + '0'
        else:
            key = key + '1'
        for i in range(0, self._board_size):
            for j in range(0, self._board_size):
                pos = (i, j)
                pos_str = '00'
                if pos in self.p1_position:
                    pos_str = '01'
                elif pos in self.p2_position:
                    pos_str = '11'
                key = key + pos_str

        return key

    @staticmethod
    def decoder(key):
        turn_player = ''
        if key[0] == '0':
            turn_player = 'player_1'
        elif key[0] == '1':
            turn_player = 'player_2'

        i, j = 0, 0
        pos_pointer = 1
        p1_position = []
        p2_position = []
        while pos_pointer < len(key):
            if key[pos_pointer:pos_pointer+2] == '01':
                # print(key[pos_pointer:pos_pointer+2], (i,j))
                p1_position = p1_position + [(i, j)]
            elif key[pos_pointer:pos_pointer+2] == '11':
                # print(key[pos_pointer:pos_pointer+2], (i,j))
                p2_position = p2_position + [(i, j)]

            pos_pointer += 2
            j += 1
            if j % GameBoard._board_size == 0:
                j = 0
                i += 1

        return GameBoard(p1_position=p1_position, p2_position=p2_position, turn_player=turn_player)

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
            valid_move_list = valid_move_list + \
                generate_moves(self, start_pos=pos)
        self.valid_move_list = valid_move_list

    def is_winning(self):
        if self.turn_player == 'player_1':
            if ((self._board_size - 1, self._board_size - 1) in self.p1_position) or (len(self.p2_position) == 1 and len(self.p1_position) > 1):
                return True
        elif self.turn_player == 'player_2':
            if ((0, 0) in self.p2_position) or (len(self.p1_position) == 1 and len(self.p2_position) > 1):
                return True
        return False

    def is_loosing(self):
        if self.turn_player == 'player_1':
            if (0, 0) in self.p2_position or (len(self.p1_position) == 1 and len(self.p2_position) > 1):
                return True
        elif self.turn_player == 'player_2':
            if (self._board_size - 1, self._board_size - 1) in self.p1_position or (len(self.p2_position) == 1 and len(self.p1_position) > 1):
                return True
        return False

    def is_draw(self):
        # both only had one piece left -> not possible
        if len(self.p1_position) == 1 and len(self.p2_position) == 1:
            return True
        # # no move is possible
        # if self.valid_move_list == []:
        #     return True
        
        return False

    def list_all_valid_moves(self):
        # valid_moves_dict = {}
        # for move in self.valid_move_list:
        #     key_str = '{}->{}'.format(move.start_pos, move.end_pos)
        #     valid_moves_dict[key_str] = move
        # return valid_moves_dict
        return self.valid_move_list

    def evaluation(self, depth=3):
        self_score = 0
        oppo_score = 0
        # If self winning
        if self.is_loosing():
            self_score += -9999999
            oppo_score += 1000

        # If self loosing
        if self.is_winning():
            self_score += 1000
            oppo_score += -9999999

        # If the game draw
        if self.is_draw():
            self_score += 100
            oppo_score += 100

        if self.turn_player == 'player_1':
            self_target = (self._board_size - 1, self._board_size - 1)
            oppo_target = (0, 0)
            self_position = self.p1_position
            oppo_position = self.p2_position

            # How many piece is still on the board
            self_piece_cnt = len(self.p1_position)
            oppo_piece_cnt = len(self.p2_position)

        elif self.turn_player == 'player_2':
            self_target = (0, 0)
            oppo_target = (self._board_size - 1, self._board_size - 1)
            self_position = self.p2_position
            oppo_position = self.p1_position

            # How many piece is still on the board
            self_piece_cnt = len(self.p2_position)
            oppo_piece_cnt = len(self.p1_position)

        # SELF - How each piece close to the target posotion => add weight
        for pos in self_position:
            diff = (abs(self_target[0]-pos[0]), abs(self_target[1]-pos[1]))
            pos_score = (self._board_size -
                         diff[0]) ** 2 + (self._board_size - diff[1]) ** 2
            self_score += pos_score

        # OPPO - How each piece close to the target posotion => add weight
        for pos in oppo_position:
            diff = (abs(oppo_target[0]-pos[0]), abs(oppo_target[1]-pos[1]))
            pos_score = (self._board_size - 1 -
                         diff[0]) ** 2 + (self._board_size - 1 - diff[1]) ** 2
            oppo_score += pos_score

        self.board_score = self_score + self_piece_cnt * 10
        self.opponent_score = oppo_score + oppo_piece_cnt * 10

### ---------------------------------------- ###
# Functions for playing the game


def is_valid(status: GameBoard, start_pos: tuple, end_pos: tuple, last_pos: tuple = None, jump_through: tuple = None, previous_steps: Move = None):
    # if move is out of border
    if end_pos[0] >= status._board_size or end_pos[1] >= status._board_size or end_pos[0] < 0 or end_pos[1] < 0:
        return False

    # if the move pos is occupied (included intermediate points and end points)
    if end_pos in status.p1_position or end_pos in status.p2_position:
        return False

    # Prevent jumping back to the start pos
    if last_pos:
        if end_pos == last_pos:
            return False

    # Prevent jumping into back patterns
    if jump_through and previous_steps:
        # print('jump_through', jump_through, 'previous_steps.jump_through_pos:', previous_steps.jump_through_pos)
        if jump_through in previous_steps.jump_through_pos or end_pos == previous_steps.start_pos:
            return False

    return True


def generate_moves(status: GameBoard, start_pos: tuple,
                   previous_steps: Move = None, is_jumping: bool = False, last_pos: tuple = None):
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

                new_status = deepcopy(status)
                # print(previous_steps)
                # If previous jumps had remove a pos
                if previous_steps is not None:
                    # print('previous remove:', previous_steps.removed_opponent_pos)
                    remove_pos = previous_steps.removed_opponent_pos
                else:
                    remove_pos = None

                # Prepare for keep jumping
                if status.turn_player == 'player_1':
                    new_status.p1_position.remove(start_pos)
                    new_status.p1_position.add(move_pos)
                    # if (not has_remove) and neighbor in new_status.p2_position:
                    if (not remove_pos) and neighbor in new_status.p2_position:
                        remove_pos = neighbor
                        # print('*** A remove:', remove_pos)
                        new_status.p2_position.remove(remove_pos)
                        # has_remove = True

                elif status.turn_player == 'player_2':
                    new_status.p2_position.remove(start_pos)
                    new_status.p2_position.add(move_pos)
                    # if (not has_remove) and neighbor in new_status.p1_position:
                    if (not remove_pos) and neighbor in new_status.p1_position:
                        remove_pos = neighbor
                        # print('*** A remove:', remove_pos)
                        new_status.p1_position.remove(remove_pos)
                        # has_remove = True

                # Add the option to the result set
                if not previous_steps:
                    move = Move(start_pos, move_pos,
                                removed_opponent_pos=remove_pos, jump_through_pos=[neighbor])
                    valid_moves = valid_moves + [move]
                else:
                    jump_through_pos = previous_steps.jump_through_pos + \
                        [neighbor]
                    move = Move(previous_steps.start_pos, move_pos,
                                removed_opponent_pos=remove_pos, jump_through_pos=jump_through_pos)
                    valid_moves = valid_moves + [move]

                # Try to keep jumping: Create a new game status for making the move:
                new_start_pos = move_pos

                valid_jump_moves = generate_moves(
                    new_status, new_start_pos, previous_steps=move, is_jumping=True,
                    last_pos=start_pos)
                valid_moves = valid_moves + valid_jump_moves

    return valid_moves


def make_a_move(board: GameBoard, move: Move):
    new_board = deepcopy(board)
    if new_board.turn_player == 'player_1':
        new_board.p1_position.remove(move.start_pos)
        new_board.p1_position.add(move.end_pos)
        new_board.turn_player = 'player_2'
        new_board.opponent_score = 'player_1'
        if move.removed_opponent_pos:
            new_board.p2_position.remove(move.removed_opponent_pos)
    elif new_board.turn_player == 'player_2':
        new_board.p2_position.remove(move.start_pos)
        new_board.p2_position.add(move.end_pos)
        new_board.turn_player = 'player_1'
        new_board.opponent_score = 'player_2'
        if move.removed_opponent_pos:
            new_board.p1_position.remove(move.removed_opponent_pos)
    return new_board


def generate_random_game(seed):
    pass
