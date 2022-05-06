
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


### ---------------------------------------- ###
# Start a game

# game = GameBoard()
# game.generate_round_moves()

# try_pos_1 = [(5, 3), (4, 5)]
# try_pos_2 = [(5, 5), (5, 4), (0, 3), (0, 2)]
# game = GameBoard(p1_position=try_pos_1, p2_position=try_pos_2, turn_player='player_1')

# random.seed(18)
# #%%
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

# print('The Winner:', game.turn_player, '; Total rounds of the game:', round)
# print('RESULT:\nP1: %s\nP2: %s'%(game.p1_position, game.p2_position))


# def session_end(game):
#     if game.is_loosing():
#         print('RESULT:\nP1: %s\nP2: %s'%(game.p1_position, game.p2_position))
#         winner = 'player_1'
#         if game.turn_player == 'player_1':
#             winner = 'player_2'
#             print('The Winner:', winner)
#     elif game.is_winning():
#         print('RESULT:\nP1: %s\nP2: %s'%(game.p1_position, game.p2_position))
#         print('The Winner:', current_player)
#     elif game.is_draw():
#         print('RESULT:\nP1: %s\nP2: %s'%(game.p1_position, game.p2_position))
#         print('DRAW!')
    
#     end_surface = pygame.Surface(WINDOWSIZE)
#     end_surface = end_surface.convert_alpha()
#     end_surface.fill((255, 255, 255, 0))
#     pygame.draw.rect(end_surface, color_gray_1, (WIDTH, HEIGHT))

# class Button:
#     # REF: https://pythonprogramming.altervista.org/buttons-in-pygame/
#     def __init__(self, text,  pos, font, bg="black", feedback=""):
#         self.x, self.y = pos
#         self.font = pygame.font.SysFont("Arial", font)
#         if feedback == "":
#             self.feedback = "text"
#         else:
#             self.feedback = feedback
#         self.change_text(text, bg)
    
#     def change_text(self, text, bg="black"):
#         """Change the text whe you click"""
#         self.text = self.font.render(text, 1, pygame.Color("White"))
#         self.size = self.text.get_size()
#         self.surface = pygame.Surface(self.size)
#         self.surface.fill(bg)
#         self.surface.blit(self.text, (0, 0))
#         self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
 
#     def show(self):
#         screen.blit(self.surface, (self.x, self.y))

#     def click(self, event):
#         x, y = pygame.mouse.get_pos()
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if pygame.mouse.get_pressed()[0]:
#                 if self.rect.collidepoint(x, y):
#                     self.change_text(self.feedback, bg="red")

# -------- Try A Given Status ----------- # 
# Input Status
# try_pos_1 = [(0, 1), (1, 1), (0, 2), (2, 2)]
# try_pos_2 = [(5, 5), (3, 1), (3, 4), (4, 3)]
# game = GameBoard(p1_position=try_pos_1, p2_position=try_pos_2, turn_player='player_1')

# player_1 = HumanPlayer(player=1)
# player_1 = RandomPlayer(player=1)
# player_2 = RandomPlayer(player=2)
# game_board_status=[[None] * GameBoard._board_size for _ in range(GameBoard._board_size)]  # Proper initialization.