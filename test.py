
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