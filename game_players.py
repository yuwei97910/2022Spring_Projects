"""
IS 597 Final Project
YuWei Lai
04.29.2022

game_players.py deals with the player clients in the game.
"""
#%%
import random
from game_module import GameBoard, Move, make_a_move

class HumanPlayer:
    """
    The game client for the Human Player
    """
    def __init__(self, player=1) -> None:
        if player == 1: 
            self.turn_player = 'player_1'
        elif player == 2: 
            self.turn_player = 'player_2'
        else:
            raise Exception('The player should be: 1 or 2.')
    
    def choose_a_move(self, board:GameBoard) -> Move:
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
    """
    The game client for the Random Player
    """
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
    """
    The game client for the Smart Player
    """
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

        valid_moves_score = {}

        best_move = None
        best_score = -1
        dominant_move = None

        # Test each move in the valid move set
        for move in board.valid_move_list: # move[0]: key; move[1]: value::Move

            # Initialzing
            # When making a move it will go into the next turn (the opponent's turn)
            temp_score = 0
            temp_board = make_a_move(board, move) # in the temp board, the player would be the opponent
            key = temp_board.encoder()
            
            # Get the evaluated score in the history
            if key in self.learned_board.keys():
                if temp_board.turn_player == opponent_player:
                    temp_score = self.learned_board[key].board_score
                elif temp_board.turn_player == opponent_player:
                    temp_score = self.learned_board[key].opponent_score
                if temp_score >= best_score:
                    best_move = move
                    best_score = temp_score

            # Initialize a best move 
            if not best_move:
                best_move = move
                temp_board.evaluation()
                if temp_board.turn_player == opponent_player:
                    best_score = temp_board.board_score
                elif temp_board.turn_player == self_player:
                    best_score = temp_board.opponent_score
            
            # Depth Search to judge a move
            depth = 1
            while depth < max_depth:                
                # In the opponent's turn, the opponent will also try to maximize their score
                if self_player != temp_board.turn_player:
                    temp_board.generate_round_moves()
                    if temp_board.is_winning() or temp_board.is_loosing() or temp_board.is_draw():
                        break
                    next_move, s = self.choose_a_move(temp_board, self_player, max_depth=max_depth-1)
                    temp_board = make_a_move(temp_board, next_move) # player change to self
                
                # In self's turn choose the maximized score move
                else:
                    temp_board.generate_round_moves()
                    if temp_board.is_winning() or temp_board.is_loosing() or temp_board.is_draw():
                        # dominant_move = move
                        break
                    next_move, s = self.choose_a_move(temp_board, self_player, max_depth=max_depth-1)
                    temp_board = make_a_move(temp_board, next_move) # player change to the opponent
                    
                depth += 1
            
            # print('The total depth', depth)
            if not dominant_move:
                temp_board.evaluation()
                self.learned_board[key] = temp_board

                if temp_board.turn_player == self_player:
                    temp_score = temp_board.board_score
                elif temp_board.turn_player == opponent_player:
                    temp_score = temp_board.opponent_score
                if temp_score >= best_score:
                    best_move = move
                    best_score = temp_score
            else:
                best_move = dominant_move
                break
        
        return best_move, best_score