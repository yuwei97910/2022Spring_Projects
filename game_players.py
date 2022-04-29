#%%
import random
# random.seed(0)
from game_module import GameBoard, Move, make_a_move

class HumanPlayer:
    def __init__(self, player=1) -> None:
        if player == 1: 
            self.turn_player = 'player_1'
        elif player == 2: 
            self.turn_player = 'player_2'
        else:
            raise Exception('The player should be: 1 or 2.')
    
    def choose_a_move(self, board:GameBoard) -> Move:
        # valid_moves_dict = board.list_all_valid_moves() # get all valid moves from a game status
        # # print([x for x in valid_moves_dict.keys()])
        # display_dict = {}
        # print("\nHuman Player's Options:")
        # for i, key in enumerate(valid_moves_dict.keys()):
        #     print('Option: %s - %s' % (i, key))
        #     display_dict[i] = key

        # chosen_key = None
        # while not chosen_key in display_dict:
        #     chosen_key = int(input('\nPlease Input A Move Option: '))
        #     if chosen_key not in display_dict:
        #         print('Please input a valid move!!!')
        # return valid_moves_dict[display_dict[chosen_key]], 0 # move

        all_valid_moves = board.list_all_valid_moves() # get all valid moves from a game status
        # print([x for x in valid_moves_dict.keys()])
        display_dict = {}
        print("\nHuman Player's Options:")
        for i, move in enumerate(all_valid_moves):
            print('Option: %s - %s->%s; Capture: %s' % (i, move.start_pos, move.end_pos, move.removed_opponent_pos))
            display_dict[i] = move

        chosen_key = None
        while not chosen_key in display_dict:
            chosen_key = int(input('\nPlease Input A Move Option: '))
            if chosen_key not in display_dict:
                print('Please input a valid move!!!')
        return all_valid_moves[chosen_key], 0 # move

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

        return board.valid_move_list[random_index], 0 # move

class SmartPlayer:
    def __init__(self, player=1) -> None:

        self.learned_board = {}

        if player == 1: 
            self.self_player = 'player_1'
        elif player == 2: 
            self.self_player = 'player_2'
        else:
            raise Exception('The player should be: 1 or 2.')

    def choose_a_move(self, board:GameBoard, self_player=None, max_depth=3) -> Move:
        if not self_player:
            self_player = self.self_player

        if self_player == 'player_1':
            opponent_player = 'player_2'
        elif self_player == 'player_2':
            opponent_player = 'player_1'

        # valid_moves_dict = board.list_all_valid_moves()
        valid_moves_score = {}

        best_move = None
        best_score = -1
        dominant_move = None

        # Test each move in the valid move set
        for move in board.valid_move_list: # move[0]: key; move[1]: value::Move
            # Initialzing
            # When making a move it will go into the next turn (the opponent's turn)
            temp_score = 0
            temp_board = make_a_move(board, move)
            key = temp_board.encoder()
            
            if key in self.learned_board.keys():
                if temp_board.turn_player == opponent_player:
                    temp_score = self.learned_board[key].board_score
                elif temp_board.turn_player == opponent_player:
                    temp_score = self.learned_board[key].opponent_score
                if temp_score >= best_score:
                    best_move = move
                    best_score = temp_score

            if not best_move:
                best_move = move
                temp_board.evaluation()
                if temp_board.turn_player == opponent_player:
                    best_score = temp_board.board_score
                elif temp_board.turn_player == self_player:
                    best_score = temp_board.opponent_score
            
            depth = 1
            while depth < max_depth:                
                # In the opponent's turn, the opponent will also try to maximize their score
                if self_player != temp_board.turn_player:
                    temp_board.generate_round_moves()
                    if temp_board.is_winning() or temp_board.is_loosing() or temp_board.is_draw():
                        break
                    next_move, s = self.choose_a_move(temp_board, self_player, max_depth=max_depth-1)
                    temp_board = make_a_move(temp_board, next_move) # player change to self

                    # Next Turn: Self
                    # if temp_board.is_winning(): # self is winning
                    #     # print('Player %s: SELF WINNING' %(temp_board.turn_player))
                    #     # dominant_move = move
                    #     break

                
                # In self's turn choose the maximized score move
                else:
                    temp_board.generate_round_moves()
                    if temp_board.is_winning() or temp_board.is_loosing() or temp_board.is_draw():
                        # dominant_move = move
                        break
                    next_move, s = self.choose_a_move(temp_board, self_player, max_depth=max_depth-1)
                    temp_board = make_a_move(temp_board, next_move) # player change to the opponent

                    # Next Turn: Opponent
                    # if temp_board.is_loosing(): # opponent is loosing
                    #     # print('Player %s: OPPONENT LOOSING' %(temp_board.turn_player))
                    #     dominant_move = move
                    #     break

                depth += 1
            
            # print('The total depth', depth)
            if not dominant_move:
                temp_board.evaluation()
                self.learned_board[key] = temp_board

                if temp_board.turn_player == self_player:
                    temp_score = temp_board.board_score
                    # temp_score = temp_board.opponent_score
                elif temp_board.turn_player == opponent_player:
                    temp_score = temp_board.opponent_score
                    # temp_score = temp_board.board_score
                if temp_score >= best_score:
                    best_move = move
                    best_score = temp_score
            else:
                best_move = dominant_move
                break
        
        return best_move, best_score


### ---------------------------------------- ###
# Start a game

# try_pos_1 = [(0, 1), (1, 1), (0, 2), (2, 2)]
# try_pos_2 = [(5, 5), (3, 1), (3, 4), (4, 3)]
# game = GameBoard(p1_position=try_pos_1, p2_position=try_pos_2, turn_player='player_1')

# game.generate_round_moves()

# game = GameBoard()
# random.seed(57)

# # HumanPlayer, SmartPlayer, or RandomPlayer
# player_1 = SmartPlayer(player=1)
# player_2 = RandomPlayer(player=2)
# # player_2 = SmartPlayer(player=2)
# round = 0
# while not game.is_draw() and not game.is_loosing():
#     current_player = game.turn_player
#     game.generate_round_moves()

#     print('\n-----------------------------\nRound: %s; Turn: %s\nP1: %s\nP2: %s' % 
#                 (round, current_player, game.p1_position, game.p2_position))

#     if current_player == 'player_1':
#         move, best_score = player_1.choose_a_move(game)
#         print('A Move - Chosen Move: ', move.start_pos, move.end_pos, 'Chosen Score: ', best_score)

#     elif current_player == 'player_2':
#         move, best_score = player_2.choose_a_move(game)
#         print('A Move - Chosen Move: ', move.start_pos, move.end_pos, 'Chosen Score: ', best_score)

#     game = make_a_move(game, move)
#     round += 1

# print('The Winner:', current_player, '; Total rounds of the game:', round)

# print('RESULT:\nP1: %s\nP2: %s'%(game.p1_position, game.p2_position))
# %%
