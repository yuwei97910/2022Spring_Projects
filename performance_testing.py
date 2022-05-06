"""
IS 597 Final Project
YuWei Lai
04.29.2022

performance_testing.py is for testing purpose.
It will generate performance reports for given rounds and player types
"""

#%%
from copy import deepcopy
import random
import time

from game_module import GameBoard, Move, make_a_move
from game_players import HumanPlayer, RandomPlayer, SmartPlayer

# --------------- #
# Given testing options
max_test = 50 # max testing rounds
file_name = 'performance_testing.txt'

ini_player_1 = RandomPlayer(player=1)
ini_player_2 = SmartPlayer(player=2)

# --------------- #
p1_winning_cnt = 0
p2_winning_cnt = 0
draw_cnt = 0

record = open(file_name, 'w')
record.write('test_round,winner,rounds,time_consumed\n')

test_round = 0
total_start = time.process_time()
while test_round < max_test:
    round_start = time.process_time()

    random.seed(test_round)
    test_round += 1
    print('\n-----------------------------\n-----------------------------\nTEST ROUND: ', test_round)

    # Test a game
    game = GameBoard()
    game.generate_round_moves()

    # initialize the players
    player_1 = deepcopy(ini_player_1)
    player_2 = deepcopy(ini_player_2)

    round = 0 # Single game rounds
    while not game.is_draw() and not game.is_loosing():
        current_player = game.turn_player

        print('\n-----------------------------\nRound: %s; Turn: %s\nP1: %s\nP2: %s' % 
                    (round, current_player, game.p1_position, game.p2_position))

        if current_player == 'player_1':
            move, best_score = player_1.choose_a_move(game)
            print('A Move - Chosen Move: ', move.start_pos, move.end_pos, 'Chosen Score: ', best_score)

        elif current_player == 'player_2':
            move, best_score = player_2.choose_a_move(game)
            print('A Move - Chosen Move: ', move.start_pos, move.end_pos, 'Chosen Score: ', best_score)

        game = make_a_move(game, move)
        game.generate_round_moves()
        round += 1

        # print('Game is draw?', game.is_draw(), game.turn_player, 'P1: ', game.p1_position, 'P2: ', game.p2_position, 'Possible Move:', game.list_all_valid_moves())

    if game.is_loosing():
        print('RESULT:\nP1: %s\nP2: %s'%(game.p1_position, game.p2_position))
        winner = 'player_1'
    if game.turn_player == 'player_1':
        winner = 'player_2'
        print('The Winner:', winner, '; Total rounds of the game:', round)
    elif game.is_winning():
        print('RESULT:\nP1: %s\nP2: %s'%(game.p1_position, game.p2_position))
        print('The Winner:', current_player, '; Total rounds of the game:', round)
        winner = current_player
    elif game.is_draw():
        print('RESULT:\nP1: %s\nP2: %s'%(game.p1_position, game.p2_position))
        print('DRAW!')
        winner = 'draw'

    if winner == 'player_1':
        p1_winning_cnt += 1
    elif winner == 'player_2':
        p2_winning_cnt += 1
    else:
        draw_cnt += 1

    round_time = time.process_time() - round_start
    record.write(('%s,%s,%s,%s\n' % (test_round, winner, round, round_time)))

total_end = time.process_time()
total_time = total_end - total_start

record.write((('Total Games: %s\n'% test_round)))
record.write((('Total Time: %s\n'% total_time)))
record.write((('Player 1 Total Wins: %s\n'% p1_winning_cnt)))
record.write((('Player 2 Total Wins: %s\n'% p2_winning_cnt)))
record.write((('Draws: %s\n'% draw_cnt)))
record.close()