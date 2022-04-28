from curses import window
import pygame
import random
# random.seed(0)
from game_module import GameBoard, Move, make_a_move
from game_players import HumanPlayer, RandomPlayer, SmartPlayer

# color
black = (0, 0, 0)
color_piece_1 = (35, 85, 110)
color_piece_2 = (170, 55, 55)
color_gray_1 = (235, 235, 235)
color_gray_2 = (201, 201, 201)
background_color = (210, 230, 230)

# https://stackoverflow.com/questions/49342252/creating-checkers-pieces-using-a-2d-array-pygame


# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 80
HEIGHT = 80
RADIUS = 35
POS_ADJUSTMENT = 40

MARGIN = 0 # This sets the MARGIN between each cell
WINDOWSIZE=[960, 640]

def square_colour(row, col):
    """ Determine colour of game board square from its position. """
    return color_gray_1 if (row + col) % 2 == 0 else color_gray_2  # Makes upper-left corner white.

def board_display(color_gray_1, color_gray_2):
    for row in range(GameBoard._board_size):
        for col in range(GameBoard._board_size):
            x_coordinate=((MARGIN + WIDTH) * col + MARGIN)
            y_coordinate=((MARGIN + HEIGHT) * row + MARGIN)
            box_color = (color_gray_2 if (row + col) % 2 == 0 else color_gray_1)

            pygame.draw.rect(screen, box_color, [x_coordinate, y_coordinate, WIDTH, HEIGHT])

def pieces_display(p1_position, p2_position, color_piece_1, color_piece_2):
    for row in range(GameBoard._board_size):
        for col in range(GameBoard._board_size):
            row_coordinate=((MARGIN + HEIGHT) * row + MARGIN + POS_ADJUSTMENT)
            col_coordinate=((MARGIN + WIDTH) * col + MARGIN + POS_ADJUSTMENT)
            
            if (row, col) in p1_position:
                pygame.draw.circle(screen, color_piece_1, (col_coordinate, row_coordinate), RADIUS)
            elif (row, col) in p2_position:
                pygame.draw.circle(screen, color_piece_2, (col_coordinate, row_coordinate), RADIUS)

def session_end(game):
    if game.is_loosing():
        print('RESULT:\nP1: %s\nP2: %s'%(game.p1_position, game.p2_position))
        winner = 'player_1'
        if game.turn_player == 'player_1':
            winner = 'player_2'
            print('The Winner:', winner, '; Total rounds of the game:', round)
    elif game.is_winning():
        print('RESULT:\nP1: %s\nP2: %s'%(game.p1_position, game.p2_position))
        print('The Winner:', current_player, '; Total rounds of the game:', round)
    elif game.is_draw():
        print('RESULT:\nP1: %s\nP2: %s'%(game.p1_position, game.p2_position))
        print('DRAW!')
    
    end_surface = pygame.Surface(WINDOWSIZE)
    end_surface = end_surface.convert_alpha()
    end_surface.fill((255, 255, 255, 0))
    pygame.draw.rect(end_surface, color_gray_1, (WIDTH, HEIGHT))


class Button:
    # REF: https://pythonprogramming.altervista.org/buttons-in-pygame/
    """Create a button, then blit the surface in the while loop"""
    def __init__(self, text,  pos, font, bg="black", feedback=""):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Arial", font)
        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        self.change_text(text, bg)
    
    def change_text(self, text, bg="black"):
        """Change the text whe you click"""
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
 
    def show(self):
        screen.blit(self.surface, (self.x, self.y))

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    self.change_text(self.feedback, bg="red")


# Input Status
# try_pos_1 = [(0, 1), (1, 1), (0, 2), (2, 2)]
# try_pos_2 = [(5, 5), (3, 1), (3, 4), (4, 3)]
# game = GameBoard(p1_position=try_pos_1, p2_position=try_pos_2, turn_player='player_1')


# player_1 = HumanPlayer(player=1)
# player_1 = RandomPlayer(player=1)
# player_2 = RandomPlayer(player=2)

game = GameBoard()
player_1 = None
player_2 = None
# game_board_status=[[None] * GameBoard._board_size for _ in range(GameBoard._board_size)]  # Proper initialization.

# -------- Main PyGame Program Loop -----------
pygame.init()
pygame.display.set_caption("The Conquer Game")

button1 = Button(
    "Click here",
    (100, 100),
    font=30,
    bg="navy",
    feedback="You clicked me")


screen = pygame.display.set_mode(WINDOWSIZE)
is_end = False
clock = pygame.time.Clock()
round = 0
while not is_end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_end = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            print(pos)

            # Change the x/y screen coordinates to grid coordinates
            column = (pos[0]) // (WIDTH+MARGIN)
            row = pos[1] // (HEIGHT+MARGIN)
        
    
    # Choose the player type when starting the game
    if player_1 is None or player_2 is None:
        print('\n-----------------------------\nPlease Choose Player Types:\n1: Human Player\n2: Smart Player\n3: Random Player\n-----------------------------')
        p1_chocie = int(input('Please Choose the Player Type for Player 1: '))
        p2_chocie = int(input('Please Choose the Player Type for Player 2: '))
        print('\n-----------------------------\n')

        if p1_chocie == 1: player_1 = HumanPlayer(player=1)
        elif p1_chocie == 2: player_1 = SmartPlayer(player=1)
        elif p1_chocie == 3: player_1 = RandomPlayer(player=1)

        if p2_chocie == 1: player_2 = HumanPlayer(player=2)
        elif p2_chocie == 2: player_2 = SmartPlayer(player=2)
        elif p2_chocie == 3: player_2 = RandomPlayer(player=2)

    # session_end(game)

    # The main operation for the game
    if round >= 1 and not game.is_draw() and not game.is_loosing():
        current_player = game.turn_player
        game.generate_round_moves()

        print('\n-----------------------------\nRound: %s; Turn: %s\nP1: %s\nP2: %s' % 
                    (round, current_player, game.p1_position, game.p2_position))

        if current_player == 'player_1':
            move, best_score = player_1.choose_a_move(game)
            print('A Move - Chosen Move: ', move.start_pos, move.end_pos, 'Chosen Score: ', best_score)

        elif current_player == 'player_2':
            move, best_score = player_2.choose_a_move(game)
            print('A Move - Chosen Move: ', move.start_pos, move.end_pos, 'Chosen Score: ', best_score)

        game = make_a_move(game, move)
    
    round += 1

    screen.fill(background_color)
    board_display(color_gray_1, color_gray_2) # Display the board
    pieces_display(game.p1_position, game.p2_position, color_piece_1, color_piece_2)

    clock.tick(60)
    pygame.time.delay(1000)
    pygame.display.flip()
    
    # ---------------------------------------- #
    # When a game is end
    if game.is_loosing() or game.is_winning() or game.is_draw():
    #     session_end(game)
        print("\n-----------------------------\nThe Game End\n-----------------------------\n")
        print('RESULT:\nP1: %s\nP2: %s\nTotal rounds of the game: %s'%(game.p1_position, game.p2_position, round))
        if game.is_loosing():
            winner = 'player_1'
            if game.turn_player == 'player_1':
                winner = 'player_2'
            print('The Winner:', winner, '; Total rounds of the game:', round)
        elif game.is_winning():
            print('The Winner:', game.turn_player)
        elif game.is_draw():
            print('DRAW!')
        
        print('\n-----------------------------\nRestart the game?\n-----------------------------\n')
        end_option = int(input('1: Restart a game; 2: End the session.\nYour Option: '))
        if end_option == 1:
            game = GameBoard()
            player_1 = None
            player_2 = None
            round = 0
        elif end_option == 2:
            is_end = True

    # button1.click(event)
    # button1.show()



pygame.quit()
