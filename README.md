# 2022 Spring IS597 Projects: The C&C Game: Capturing and Conquering Game
#### April 29, 2022

### Yu-Wei Lai (yuwei6@illinois.edu)

----

# Introduction
C&C Game: Capturing and Conquering Game

The idea of the game is from Chinese Checkers, Halma Game, and English Checkers. There are several adjustments made to the game. For example, compared to Halma, **capturing** is added. Compared to Chinese Checker, the game plays on a square board, so more possible directions are added. Also, compared with English Checkers, **jumping moves can be continued** and more directions as well.

#### The Game Board
<p align="center"><img width="480" alt="image" src="https://user-images.githubusercontent.com/29009521/165926820-20f00b0e-70de-4e59-922b-4e17b7ea6e81.png"></p>

## Game Rules
The game can be started with a board size of 6\*6 or 8\*8. The player who plays with the left-upper side (blue pieces) plays first.

### Winning Condition
1. The player occupies the **target position**.
2. The player *makes the opponent have only one piece left on the board*, and the player still has more than one-pieces.

<p align="center"><img width="772" alt="image" src="https://user-images.githubusercontent.com/29009521/167103305-660eca6d-95a0-4310-a11d-2824a09e79bb.png"></p>


#### Target Position
The farthest position on the diagonal line.

In a 6 * 6 setting game, for Player 1 (the left upper player), the target position is (6, 6). The target position for Plyer 2 (the right lower player) would be (0, 0).

<p align="center"><img width="499" alt="image" src="https://user-images.githubusercontent.com/29009521/167103355-6a0d8e99-5adb-4774-9a31-57c9c6849971.png"></p>

#### Draw?
1. The first setting of the draw condition would be both players have only one piece left on the board. However, it will not happen with the current rules of the game since the previous stage would be a winning condition for another player.
2. One player may have no possible move. In this condition, it should be a draw. For example, player 1 occupies (5, 3), (4, 5), and player 2 occupies (5, 5), (5, 4). The next turn comes to player 1, and the player will have no valid moves.

### How to move?
There are two kinds of moving methods: (1) Normal Move and (2) Jumping Move. A player can only place a normal move in a round but several jumping moves in a single round. However, when the player places a normal move, the player cannot go on a jumping move in that round. On the other hand, there is **capturing** included in the jumping moves.

#### How to move: Normal Move
In the normal move, a player can only move in the direction that getting closer to the target position. When moving in the normal move method, the player can only move one time in a single round. There are three possible directions.

<p align="center"><img width="376" alt="image" src="https://user-images.githubusercontent.com/29009521/167103163-cd3b8529-894d-44be-9245-e2e1d430b8df.png"></p>

#### How to move: Jumping Move
The jumping idea is similar to the Halma Game or English Checkers. A piece can jump over the pieces which are in its neighbors; that is, eight possible directions. A piece can jump over both self-player's pieces and opponent's pieces. Jumping moves can be continued, and the plyer can choose which position to stop. 

##### Capturing
Also, the game includes a **capturing** in a jumping move. When a piece jumps over any opponent's pieces, the first opponent's piece is captured. In each round, there is only at most one piece is captured.

<p align="center"><img width="876" alt="image" src="https://user-images.githubusercontent.com/29009521/167117587-d46e44ad-83a5-40d2-b00e-d23e1786051d.png"></p>

> Assuming it is the turn for the blue player, and the player would like to play on the piece on (1, 2). There are 14 possible move methods for this single piece. The star is the starting position in the image, and the yellow circles are the possible ending positions. The blue triangle is the possible captured piece. One normal move is identified with the green circle.

----

## How to start the game?
### Starting the app (The complete GUI for the game is not complete!)
*At the current stage, you should run the main.py file with the command line.*
After that, the app will ask you to choose the player types for Player 1 and Player 2.
Both Player 1 and Player 2 can be one of the three types, so you can choose to play with a random computer, a smarter computer, or even another human.

Belows is the message from the app:

<p align="center"><img width="400" alt="image" src="https://user-images.githubusercontent.com/29009521/167103457-59732add-8008-4da5-89f8-75da79f28b1e.png"></p>

There are three options:
1. Human Player: a human can decide which step to take.
2. Smart Player: a computer player which will play with smarter strategy based on current game status.
3. Random Player: a computer player which will randomly pick a random move.

After picking up the player types, the game will start (GUI will show up after this).

As a human player, the user has to pick a move by inputing the option in each turn.

<p align="center"><img width="400" alt="image" src="https://user-images.githubusercontent.com/29009521/167103482-df059161-88b6-46c0-9534-6afb01afb1b3.png"></p>

When a game ends, the app will ask you to restart a game or not:
<p align="center"><img width="400" alt="image" src="https://user-images.githubusercontent.com/29009521/167103629-e7bac9b2-ff3e-48ba-88f7-1bf0ce0699e0.png"></p>

----
# Technical Side of The Game
## GUI
The GUI of the game is built with `PyGame`.

![image](https://user-images.githubusercontent.com/29009521/167118583-3d3bad27-c347-4027-ba8e-2f8dff464ae9.png)

## The program
### Classes
#### Board and Moves
- `Move`: class records and deals with moves.
- `GameBoard`: a class deals with a game status, including the players' positions, a score of the current status
  - `encoder()` and `decoder()`: for hashing in recording game status. It is used for smart players when learning (depth searching) how to move. By the implementation, I aimed to reduce the cost of evaluation.

#### Players
- `HumanPlayer`: the client deals with the human user as a player.
- `RandomPlayer`: the client to deal with a random player.
- `SmartPlayer`: the client deals with the smart player.
Each class is dealing how players play with each other. There is a function `choose_a_move()` included in each class. Depending on the player type, the way and logic of making a move are quite different:
- `HumanPlayer.choose_a_move()`: O(n), it takes O(n) to list out and visualizes all possible moves, where *n* should be considered as the number of all possible moves. The function will list out all options to the user and makes moves by the user's input options.
- `RandomPlayer.choose_a_move()`: O(1); The function will randomly pick a move in the valid moves set (which is already generated by another function `generate_moves()`. Please refer to the part "Functions".)
- `SmartPlayer.choose_a_move()`: O(n<sup>depth</sup>); Please refer to the part "Functions" and "The Smart Player".

### Functions
- `is_winning()`: O(1); Test the board status to see if it matches the winning/losing condition.
- `is_valid()`: O(n); Test the board status to see if a move is valid or not. (where n is the board size.)
- `generate_moves()`: 
    O(n<sup>2</sup>); Generate all possible moves for the player in a given game status. (where n should be the number of pieces, but if n as the board size is still a valid statement.) The function includes two operations:
    1. Normal Moves: where takes O(1) complexity. The function generate_moves( ) deals with normal moves by trying three neighbor directions.
    2. Jumping Moves: where takes O(n<sup>2</sup>) complexity. The function `generate_moves()` deals with the jumping move, using a brute force searching process to get all valid end positions.
- `make_a_move()`: 
    O(n); Change Game status with a valid move, and it will generate another game status. `deepcopy()` would take O(n) complexity. (where n is the board size.)

----
## Process of a round
For each move, the app will list out all valid moves for the turn players. After 

### Algorithms for generating moves
As mentioned, the moves are generated by `generate_moves()`. 
There are two parts for generating moves: (1) part for Normal Moves (2) part for Jumping Moves.

#### Algorithms for getting normal moves
- Complexity: O(1)
The function `generate_moves()` where dealing with normal moves basically try three directions for self-player's positions.

#### Algorithms for getting jumping moves
- Complexity: O(n<sup>2</sup>)
When starting a jump, the function `generate_moves()`, which deals with the jumping move, will start with a brute force searching process to get all valid end positions. 
The function will generate and record all possible moves.

-----
## The Smart Player
The smart player is built aiming to play better than random when competing with a human player. As mentioned, the move choosing process by the smart player is realized by the function `SmartPlayer.choose_a_move()`, where a mini-max-like algorithm is included. Depth is the thinking depth of the Smart Player. In the Current setting, the depth is three.

- Complexity: O(n<sup>depth</sup>)

For making each move, the smart player will think three steps further. It will consider and evaluate each board after moves. For each stage, it will choose the best score for the move. The evaluation is defined by the given strategies that we will discuss further. Also, it assumes that the opponent plays with the same strategy.

### Strategies for The Smart Player
These are the concepts for implementing the Samrt Player:
1. Reduce opponents' pieces
2. Get closer to the target position
3. Prevent itself from being captured by the opponent
4. *Prevent the opponent from getting closer to the target point*
5. *Prefer a strong structure with pieces' connection*

#### 1. Reduce the Opponent's pieces
A board with more self's pieces and less Opponent's pieces would get a higher score. Weighting for the number of pieces is included in the evaluations.

#### 2. Get closer to the target position
Distance to the target position is included in the evaluations.

#### 3. Prevent itself from capturing by the Opponent
If a player loses a piece on the board, the evaluation includes the score reduction.

#### Performance of the Smart Player's Implementation

```
Total Games: 50
Total Time: 7744.0971930000005
Smart Players Total Wins: 33
Smart Players Total Looses: 17
Draws: 0
```
The result suggested that the Smart Player can dominate the Random Player. The reason might be that there are tons of possible moves after the mid-stages of the game. Some moves might be strictly better than the others. Also, the game can be considered *irreversible* to previous stages by further moving. Therefore, if the AI player can capture some of these patterns, it can play far better than randomly.

However, this does not apply to competing with human players. The reason is that humans can think more further steps and adjustable strategies than the AI player. Further tests should be included.

#### The Smart Player is Time Consuming

- The average time per game for a random player competeing with a random player: 0.1 secs.
- The average time per game for a smart player competeing with a random player: 20 secs.

-----
## Overall Performance Report
Using PyCharm Profile:

```
Total Games: 1
Total Time: 371.017855
Smart Players Total Wins: 1
Smart Players Total Looses: 0
```
The Profile Report (sorted by Time (ms))

<p align="center"><img width="1365" alt="image" src="https://user-images.githubusercontent.com/29009521/167103859-148c2bb3-ba0b-47af-afe5-5dc8bbf034ac.png"></p>

The Profile Report (sorted by Own Time (ms))

<p align="center"><img width="1365" alt="image" src="https://user-images.githubusercontent.com/29009521/167103922-7d444913-da9a-4f5f-a510-d477870eef2d.png"></p>

This is the result of running one single game with Player 1 as the Smart Player and Player 2 as the Random Player. As the report suggested, most of the time is spent on `choose_a_move()` for choosing a move by the Smart Player. This is because of the recursive call for the depth search to generate the best move. However, in that function, we can see that most of the time is spent on `deepcopy()`, which is used to generate the game's deeper status. It should be used to prevent the reversion of the original stage, which does not truly make some moves. In conclusion, the recursive method is quite costly for tons of possible moves, and it is inevitable to prevent using `deepcopy()` for this case. We should consider less depth and a better evaluation for a move for further improvement.

Also, `GameBoard.generate_round_move` was called numerous times to generate all possible moves. The method in `class: GameBoard` will use the function `generate_move()` to generate moves. As mentioned, the function `generate_move()` includes two parts: (1) normal move and (2) jumping move. When generating the jumping moves, it also includes recursive calls. This is why the number of calling `generate_move()` is larger than the number of calling `GameBoard.generate_round_move`.

-----
# Other Topics
## Are there first-mover advantages?
### Compete between two random players for 1000 rounds:

Player 1 is the Smart Player and Player 2 is the Random Player:

```
Total Games: 1000
Total Time: 100.71785899999999
Smart Players Total Wins: 510
Smart Players Total Looses: 490
Draws: 0
```

From the result, we can see that the winning for Player 1 and Player 2 are both close to 50%.
There is no significant advantages for the player orders.

### Compete between two AI players for 50 rounds:

Both Player 1 and Player 2 are the Smart Player.
```
Total Games: 50
Total Time: 7499.822007
Player 1 Total Wins: 0
Player 2 Total Wins: 50
Draws: 0
```

#### Why Player 2 always win?
In current settings, there is no randomization included in the Smart Player. Therefore, if two Smart Players are playing, it will always end in the same status because of the defined strategies for evaluation.

The status will always be:

<p align="center"><img width="483" alt="image" src="https://user-images.githubusercontent.com/29009521/167117657-0cd3032d-0e8f-4a72-bb53-d708952e5d6b.png"></p>

-----
# Future Improvement
## A Better GUI
A GUI that do not require the command line. Player can drag the pieces directly to make a move.

## A Faster Smart Player
As mentioned, currently, the Smart Player takes time to generate moves, especially in the mid-stages of the game. Too many possible moves are included, and the deep-searching recursive calls for evaluations for each would be very costly. If a better evaluation method is included, we may consider not going through a deep search.

For the second solution, we can also consider a memory-based player. We can train the smart player with numerous games and make it memorize what the best actions are in a given stage. 

#### No searching for a dominant move
In current setting, it is interesting that the Smart Player does not take the winning immediately, and it is because of considering the next opponent's move. In this case, we should let it choose the move which directly wins a game.

## An adjustable board size with the smart palyer
In current settings, the board size is defined in the `class: GameBoard` and the size constant is changable. However, when the board size getting larger, the Smart Player cannot generate the moves in the reasonable time. The reason might be that too many possible status in the mid-stages of the game. This improvement shoulf compiled with the faster AI player mentioned above.

-----
# Reference
- Halma - play free online games. Addicting Games. (2021, April 1). Retrieved May 6, 2022, from https://www.addictinggames.com/puzzle/halma 
johnmaf23johnmaf23                    3155 bronze badges, &amp; martineaumartineau                    112k2323 gold badges152152 silver badges277277 bronze badges. 
- Creating checkers pieces using a 2D array - pygame. Stack Overflow. Retrieved May 6, 2022, from https://stackoverflow.com/questions/49342252/creating-checkers-pieces-using-a-2d-array-pygame 
- Chinese checkers. Wikimedia Foundation. (2022, April 13). Wikipedia. Retrieved May 6, 2022, from https://en.wikipedia.org/wiki/Chinese_checkers

-----
# *Project Requirement*
> # 2022 Spring Projects Description
>Each project from this semester is a public fork linked from this repository.  This is just one of the many assignments students worked on for the course, but this is the *only* one they are permitted to publish openly.
>## Final Project Expectations:
>You have considerable flexibility about specifics and you will publish your project openly (as a fork .from here) to allow making it part of your portfolio if you choose.  You may work alone or in a team of two students. 
>
>Regardless of topic, it must involve notable amounts of original work of your own, though it can of course use existing libraries or be inspired by or adapted from some other published work(s). 
>
>PLAGIARISM IS NOT ACCEPTABLE. From the first commit through all production of documentation and code, it must be crystal clear which, if any, parts of the project were based on or duplicated from any other source(s) all of which must be cited.  This should be so specific that any evaluator can tell which lines of code are original work and which aren't.  Same for all written narrative, documentation, images, significant algorithms, etc.
>
>## Project Types you may choose:
>
>(Making original _variations_ of puzzles and games isn't as difficult as it may seem -- we'll discuss this in class. _Though admittedly, making *good* game variations -- that are well-balanced, strategically interesting, with good replay value_ can take expertise or luck and play-testing with revisions.  Such balanced elegance is desirable but might not be achievable here, given the short time you have.)
>
>1. Devise your own new _original_ type of logic puzzle or an _original variation_ of existing puzzle type. Like with previous homework, your program should be able to randomly generate many puzzles of your type and to verify that all puzzles generated comply with the standard meta-rule that only one valid solution exists. It needs to output the unsolved puzzles in a way that a human can print or view them conveniently to try solving them and to somehow output (to file?) or display the solution for each puzzle when requested, so as not to spoil the challenge. An interactive UI to "play" the puzzles interactively is *not* required.
>
>2. OR develop an AI game player for an _original variation_ of some existing strategy game.  If you do this, it needs to be set up so it can either play computer-vs-computer and/or against human players with a reasonable text or graphical UI. 2B. If two teams want to independently develop AI players for the same type of game variant as each other (but using different algorithms, strategies, and/or data structures) so they can compete, that is okay.  A sub-variation is to enable this game type on our course game server, discuss with the instructor if this is of interest.
>
>3. OR Computationally 'Solve' a game.  _Background: Some strategic games, especially those of perfect information are known to be "solved". See https://en.wikipedia.org/wiki/Solved_game, which we discussed in class._  Sometimes these proofs are done through mathematical analysis, other times through exhaustive computational verification. If you choose this option, you can either write your own code or modify some existing code that plays a game, to exhaustively analyze a game to attempt to prove if it is "solved" in this way for certain configurations. Changes to rules or conditions of a known solved game can alter this outcome and require reanalysis.
>
>## Deliverables and other Requirements:
>
>* Have some fun!
>* In your own fork, please replace this README.md file's contents with a good introduction to your own project. 
>* Targeted Algorithm Analysis:  Regardless of which option you choose, you need to _describe the performance characteristics of some critical parts of your program and explain why you chose the data structures and core algorithm(s) you did_. So for example, if you chose Type #1, what's the Big-O, Big-Theta, or Big-Omega run-time complexity of your puzzle solver? Or the puzzle generator? If you're doing Type #2 and using minimax or similar, what's the complexity of your heuristic evaluation function?  
>* Performance Measurement: Supplement the analysis above with run-time measurements of multiple iterations of the game or puzzles as discussed in class.
>* If your team has more than one student, see that everyone makes substantial git commits. In addition, your README documentation should include a summary of how you shared the work.
>* Live in-class presentation & demonstration of your work.
