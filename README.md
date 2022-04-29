# 2022 Spring Projects: The Conquering Game
April 29, 2022
Yu-Wei Lai

----

# Introduction
The idea of the game is from 


## Game Rules
### Winning Condition
1. The player occupy the **target position**.
2. The player *make the opponent have only one piece left on the board*, and the player has still more than one pieces.

#### Target Position
The farest position on the diagonal line.
In a 6 * 6 setting game, for Player 1 (the left upper player), the target position is (6, 6). For Plyer 2 (the right lower player), the target position would be (0, 0).


#### Draw?
The original setting of the draw condition would be both players have only one piece left on the board. However, in the current design of the game it will not happen.

### How to move: Normal Move
In normal move, a player can only move in the directions that getting closer to the target position. When moving in normal move method, the player can only move one time in a round.



### How to move: Jumping Move


## How to start the game?
### Starting
At current stage, you should run the main.py file with the command line. 
After that, the app will ask you to choose the player types for Player 1 and Player 2.
Both Player 1 and Player 2 can be one of the three types, so you can choose to play with a randoming computer, a smarter computer, or even another human.

Belows is the message from the app:

There are three options:
1. Human Player: a human can decide which step to take.
2. Smart Player: a computer player which will play with smarter strategy based on current game status.
3. Random Player: a computer player which will randomly pick a random move.

After picking up the player types, the game will start (GUI will show up after this).

-----
## Technical Side of The Game
### GUI

### Basic Process
For each move, the app will list out all valid moves for the turn players.

### Algorithms for getting normal moves
- Complexity: O(n)


### Algorithms for getting jumpging moves
- Complexity: O(n^2)

### Algorithms for 


-----
## The Smart Player


### Strategy of The Smart Player
1. Reduce opponents' pieces
2. Get closer to the target position
3. Prevent itself from caturing by the opponent
4. Prevent opponent get close to the point
5. Prefer a strong structure with connect

#### 1. Reduce Opponent's pieces
#### 2. Get Closer to the target position
#### 3. Prevent itself from caturing by the opponent
#### 4. 


### Performance of The Smart Player
#### Rounds Consuming:
- The rounds count for a random player competeing with a random player: 0.1 secs.
- The rounds count for a smart player competeing with a random player: 20 secs.

#### Time Consuming:
- The average time per game for a random player competeing with a random player: 0.1 secs.
- The average time per game for a smart player competeing with a random player: 20 secs.


-----
## Other Topics
### Is there some first-mover advantages?
#### Compete between two random players for 1000 rounds:

```
Total Games: 1000
Total Time: 100.71785899999999
Smart Players Total Wins: 510
Smart Players Total Looses: 490
Draws: 0
```

From the result, we can see that the winning for Player 1 and Player 2 are both close to 50%.
There is no significant advantages for the player orders.

### 


-----
## Future Improvement
### A complete GUI


### A faster smart player


-----
# 2022 Spring Projects Description
Each project from this semester is a public fork linked from this repository.  This is just one of the many assignments students worked on for the course, but this is the *only* one they are permitted to publish openly.

## Final Project Expectations:
You have considerable flexibility about specifics and you will publish your project openly (as a fork from here) to allow making it part of your portfolio if you choose.  You may work alone or in a team of two students. 

Regardless of topic, it must involve notable amounts of original work of your own, though it can of course use existing libraries or be inspired by or adapted from some other published work(s). 

PLAGIARISM IS NOT ACCEPTABLE. From the first commit through all production of documentation and code, it must be crystal clear which, if any, parts of the project were based on or duplicated from any other source(s) all of which must be cited.  This should be so specific that any evaluator can tell which lines of code are original work and which aren't.  Same for all written narrative, documentation, images, significant algorithms, etc.

## Project Types you may choose:

(Making original _variations_ of puzzles and games isn't as difficult as it may seem -- we'll discuss this in class. _Though admittedly, making *good* game variations -- that are well-balanced, strategically interesting, with good replay value_ can take expertise or luck and play-testing with revisions.  Such balanced elegance is desirable but might not be achievable here, given the short time you have.)

1. Devise your own new _original_ type of logic puzzle or an _original variation_ of existing puzzle type. Like with previous homework, your program should be able to randomly generate many puzzles of your type and to verify that all puzzles generated comply with the standard meta-rule that only one valid solution exists. It needs to output the unsolved puzzles in a way that a human can print or view them conveniently to try solving them and to somehow output (to file?) or display the solution for each puzzle when requested, so as not to spoil the challenge. An interactive UI to "play" the puzzles interactively is *not* required.

2. OR develop an AI game player for an _original variation_ of some existing strategy game.  If you do this, it needs to be set up so it can either play computer-vs-computer and/or against human players with a reasonable text or graphical UI. 2B. If two teams want to independently develop AI players for the same type of game variant as each other (but using different algorithms, strategies, and/or data structures) so they can compete, that is okay.  A sub-variation is to enable this game type on our course game server, discuss with the instructor if this is of interest.

3. OR Computationally 'Solve' a game.  _Background: Some strategic games, especially those of perfect information are known to be "solved". See https://en.wikipedia.org/wiki/Solved_game, which we discussed in class._  Sometimes these proofs are done through mathematical analysis, other times through exhaustive computational verification. If you choose this option, you can either write your own code or modify some existing code that plays a game, to exhaustively analyze a game to attempt to prove if it is "solved" in this way for certain configurations. Changes to rules or conditions of a known solved game can alter this outcome and require reanalysis.


## Deliverables and other Requirements:

* Have some fun!
* In your own fork, please replace this README.md file's contents with a good introduction to your own project. 
* Targeted Algorithm Analysis:  Regardless of which option you choose, you need to _describe the performance characteristics of some critical parts of your program and explain why you chose the data structures and core algorithm(s) you did_. So for example, if you chose Type #1, what's the Big-O, Big-Theta, or Big-Omega run-time complexity of your puzzle solver? Or the puzzle generator? If you're doing Type #2 and using minimax or similar, what's the complexity of your heuristic evaluation function?  
* Performance Measurement: Supplement the analysis above with run-time measurements of multiple iterations of the game or puzzles as discussed in class.
* If your team has more than one student, see that everyone makes substantial git commits. In addition, your README documentation should include a summary of how you shared the work.
* Live in-class presentation & demonstration of your work.
