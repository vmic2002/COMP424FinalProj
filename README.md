# Colosseum Survival!

Our approach to the problem was to implement a greedy best-first search algorithm. Starting from the initial position, the agent traverses every possible (r,c) using breadth-first search on the board as long as the number of hops to reach there is not greater than the max number of steps. Within the breadth-first search algorithm, once the agent reaches a possible position (r,c), it simulates making a move there and adding a wall in all 4 positions (if possible) and calls a function f = h (which returns a low number if this is a good game state and a high number otherwise). For every possible (r,c) that can be reached (without going over max_step) and wall_dir that is valid, the value f for that possible move is recorded and we keep track of the lowest f and its accompanying new position and wall direction. Once the BFS algorithm terminates (all possible (r,c) within max_step have been reached and all 4 possible placements of walls at those (r,c) have been tried), the new position and wall_dir associated with the lowest f value is returned from the step function, ensuring that the AI agent always picks the move that minimizes f.

The agent’s design can best be described by first going over the step function and how it is implemented. Since we are using breadth-first search (https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/) , we first initialize an empty queue as well as a set of visited nodes to prevent cycles. Note that we are not simply performing BFS, but rather depth-limited BFS, where the depth limit is equal to the maximum number of steps we can take. The starting node in the graph traversal is my_pos, or the agent’s current position before attempting to make a move. Three variables must be initialized before entering the main while loop of BFS: the best new position, the best wall_dir, and the best (lowest) f value. Within the while loop, we fetch all possible immediate neighboring positions from the position we are currently at in the BFS traversal and add them to the queue and the list of visited nodes. These immediate neighbors are simply all the possible new (r,c) that my agent could move to in one hop without running into the adversary or a wall. The code from the random_agent was very helpful for this part. These neighbors are fetched by calling the getAllPossiblePositionsOneHopAway function.


Once we dequeue a node, we simulate adding a wall in all of the 4 possible places on the chess_board (as long as there isn’t already a wall there) and gather what the f value would be if our agent placed a wall there. If the f value is smaller than the current best f value, then we update the f value, best wall_dir, and the best new position.
We are able to simulate adding a wall to the chessboard by calling the f function, which takes the chessboard, the position our agent is trying, the adversary’s position, and the wall_dir our agent is trying. The f function simulates adding a wall to the chessboard by adding a wall to the chessboard at the desired position and direction, calling the heuristic function for the chessboard which contains this new wall, then removing the wall once the heuristic function is called. The heuristic function returns a value which represents how good of a choice it would be to add a wall at the desired location and wall_dir. Adding a wall to the chessboard actually means setting two values to True in the chessboard (assuming the wall is not on the edge of the board). This is because all walls (in the middle of the chessboard) are double counted! So for example, if we want to add a wall at (r,c) in the up direction, then we must also add a wall at (r-1,c) in the down direction. Even though we set two different values to true in the chessboard variable, only one wall was actually added. To remove the wall after h has been called, simply set both of those values in the chessboard back to false.
To summarize, our agent uses greedy best first search (https://www.codecademy.com/resources/docs/ai/search-algorithms/greedy-best-first-search) as a search method and attempts all possible moves by traversing the board using depth limited breadth-first search and trying to place walls in every possible position. The reason that our agent uses greedy best first search is because the f function is simply equal to h. In other words, the value that the f function returns, or the value that our agent uses to make its decision over which move to take, is simply the value that the heuristic function returns when simulating that move.
Our agent employs a heuristic-based search algorithm, specifically ‘Greedy Best-First Search’. Two primary functions: ‘h ()’ (the heuristic function) and ‘flood_fill ()’(Baeldung, Flood- Fill Algoritm) encapsulate the core of our agent’s decision-making process’.
The flood_fill () function, using a breadth-first search algorithm, calculates the accessible area from the player's position on the chessboard. The chessboard is represented as a 3D array, where each cell corresponds to a board position, and its value shows walls in four directions. This function starts by determining the chessboard’s sizes and initializes a set to track visited squares. It uses a queue to manage positions for explorations, starting with the agent’s current position and pushing and popping positions to and from the queue. For each position dequeued, it checks the adjacent squares in all four directions. If a square is within bounds, not blocked by a wall, and not already visited, it is added to the queue for further exploration. Squares are marked as visited when they’re encountered. This prevents the function calls from redundant checks and

getting stuck in an infinite loop. The total number of squares visited gives us the contiguous accessible area from the starting position, which the function returns as an integer. By implementing a version of this algorithm, our agent can effectively assess its spatial control on the chessboard, which is a significant aspect of the game's strategy. For example, this allows our agent to prioritize moves that lead to a favorable division of our board, constantly ensuring more moves on our side. This understanding of controlled space directly feeds into the heuristic function h (), influencing the agent's decisions. For instance, maintaining a distance from the opponent might show a defensive play, while controlling a larger area could be an offensive strategy.
The h () function is a cornerstone of our search algorithm, designed to evaluate and guide strategic decisions. This function operates by taking several key parameters that reflect the game's current state, including the player and adversary positions, proposed wall direction, and the agent's starting position. At the highest level, the function does a dynamic assessment of the game phase—distinguishing between early and late stages. This determination is pivotal as it influences the algorithm’s focus, transitioning from exploration and control in the early phase to space domination and avoiding confinement in the later stages. Our function uses constants c1, c3 and c4 to achieve this, each with a different strategic purpose.
Constant c1 (Player Distance Weight): This constant scales the heuristic score based on the distance between the player and the adversary. It is calculated by measuring the Manhattan distance (sum of the absolute differences in their respective coordinates) between the two players' positions. The idea is to adjust strategies based on proximity to the opponent, influencing moves towards or away from them.
Constant c3 (Controlled Area Weight): Linked directly with the output of flood_fill (), c3 inversely weighs the number of accessible squares from the player's position. A higher number of accessible squares (showing greater control of the board) results in a lower (more favorable) heuristic score. This encourages the agent to make moves that expand its territory and restrict the opponent's movement and promote an aggressive gameplay.
Constant c4 (Trapped Penalty Weight): This weight is applied if the agent is nearly trapped, specifically when surrounded by three walls. It's calculated by summing the boolean values (True/False) showing walls around the player's current position. If the sum equals or exceeds three, showing the player is nearly trapped, a significant penalty is added to the heuristic score, guiding the agent to avoid such positions. This factor is crucial and carries a greater effect in the late game phases. In the absence of it, we observed that, even though we retained more space control (owing to flood-fill algorithm), as a human agent it was relatively easy to box the student agent in when the walls are dense. This acts as a key defense for our agent.

Finally, to determine the “optimal” combination for the constants in h (), we adopted an empirical approach. We isolated each constant (c1, c3, and c4) and ran numerous autoplay sessions of our student_agent against random_agent and observed fluctuations in our win rate. By systematically tweaking these constants, we observed their impact on the agent's performance. This iterative process, involving analyzing outcomes and adjusting the constants, led us to the current configuration that consistently yielded the best results, ensuring a balanced strategy that addresses distance management, area control, and entrapment avoidance.

Main repo: https://github.com/dmeger/Project-COMP424-2023-Fall


**Project Description & Template** : https://www.overleaf.com/read/vnygbjryrxrt#7b70cb

<p align="center">
  <img src="https://cdn.britannica.com/36/162636-050-932C5D49/Colosseum-Rome-Italy.jpg?w=690&h=388&c=crop">
</p>

## Setup

To setup the game, clone this repository and install the dependencies:

```bash
pip install -r requirements.txt
```

## Playing a game

To start playing a game, we will run the simulator and specify which agents should complete against eachother. To start, several agents are given to you, and you will add your own following the same game interface. For example, to play the game using two copies of the provided random agent (which takes a random action every turn), run the following:

```bash
python simulator.py --player_1 random_agent --player_2 random_agent
```

This will spawn a random game board of size NxN, and run the two agents of class [RandomAgent](agents/random_agent.py). You will be able to see their moves in the console.

## Visualizing a game

To visualize the moves within a game, use the `--display` flag. You can set the delay (in seconds) using `--display_delay` argument to better visualize the steps the agents take to win a game.

```bash
python simulator.py --player_1 random_agent --player_2 random_agent --display
```

## Play on your own!

To take control of one side of the game and compete against the random agent yourself, use a [`human_agent`](agents/human_agent.py) to play the game.

```bash
python simulator.py --player_1 human_agent --player_2 random_agent --display
```

## Autoplaying multiple games

There is some randomness (coming from the initial game setup and potentially agent logic), so go fairly evaluate agents, we will run them against eachother multiple times, alternating their roles as player_1 and player_2, and on boards are drawn randomly (between size 6 and 12). The aggregate win % will determine a fair winner. Use the `--autoplay` flag to run $n$ games sequentially, where $n$ can be set using `--autoplay_runs`.

```bash
python simulator.py --player_1 random_agent --player_2 random_agent --autoplay
```

During autoplay, boards are drawn randomly between size `--board_size_min` and `--board_size_max` for each iteration. You may try various ranges for your own information and development by providing these variables on the command-line. However, the defaults (to be used during grading) are 6 and 12, so ensure the timing limits are satisfied for every board in this size range. 

**Notes**

- Not all agents supports autoplay. The variable `self.autoplay` in [Agent](agents/agent.py) can be set to `True` to allow the agent to be autoplayed. Typically this flag is set to false for a `human_agent`.
- UI display will be disabled in an autoplay.

## Develop your own general agent(s):

You need to write one agent and submit it for the class project, but you may develop additional agents during the development process to play against eachother, gather data or similar. To write a general agent:

1. Modify **ONLY** the [`student_agent.py`](agents/student_agent.py) file in [`agents/`](agents/) directory, which extends the [`agents.Agent`](agents/agent.py) class.
2. Do not add any additional imports.
3. Implement the `step` function with your game logic. Hint, there is plenty of useful code to get you started in the random_agent.py, and it's usually a good idea to re-use logic and functions from world.py (you can't import either file, but you can copy elements into yours).
4. Test your performance against the random_agent with ```bash
python simulator.py --player_1 student_agent --player_2 random_agent --autoplay```
5. Try playing against your own bot as a human. Consistently beating your own best-effort human play is a very good indicator of an A performance grade.

## Advanced and optional: What if I want to create other agents and test them against eachother?

There can only be one file called student_agent.py, and that's already perfectly set up to interact with our code, but you may create other agents during development. To get new files interacting correctly, you need to change a few specific things. Let's suppose you want to create second_agent.py, a second try at your student agent.

1. Create the new file by starting from a copy of the provided student_agent. ```bash cp agents/student_agent.py agents/second_agent.py```
2. Change the name in the decorator. Edit (@register_agent("student_agent")) instead to @register_agent("second_agent"), and the class name from `StudentAgent` to `SecondAgent`. 
3. Import your new agent in the [`__init__.py`](agents/__init__.py) file in [`agents/`](agents/) directory, by adding the line `from .second_agent import SecondAgent`
4. Now you can pit your two agents against each other in the simulator.py by running ```bash python simulator.py --player_1 student_agent --player_2 second_agent --display``` and see which idea is working better.
5. Adapt all of the above to create even more agents
    
## To wrap up and get ready to submit, prepare the strongest player you have found in the student_agent.py file, to be handed in for performance evaluation:

You will submit only one code file for grading: student_agent.py. Here are a few last minute things to double-check, since your agent must follow some special rules to make it possible to run in auto-grading. Failing to follow the instructions below precisely risks an automatic assignment of "poor" for the performance grade as we don't have time to debug everyone's solution.

0. Set up your authors.yaml and report PDF following the Overleaf (PDF) instructions. Then finalize this code.
1. Check that you didn't modify anything outside of student_agent. You can use git status and git diff for this.
2. Ensure student_agent does not have any additional imports.
3. The `StudentAgent` class *must be* decorated with exactly the name `student_agent`. Do not add any comments or change that line at all, as we will be interacting with it via scripting as we auto-run your agents in the tournament. (Common mistake if you did most of your dev in a differently named file, best_agent, or similar, and then copied the contents without checking).
4. You can add other variables and helper functions within the file, either inside the StudentAgent class, or at global scope.
5. Check the time limits are satisfied for all board sizes in the range 6-12, inclusive.
6. As a final test before submitting, make 100% sure the player you wish to be evaluated on runs correctly with the exact command we'll use in auto-grading ```python simulator.py --player_1 random_agent --player_2 student_agent --autoplay```

## Full API

```bash
python simulator.py -h       
usage: simulator.py [-h] [--player_1 PLAYER_1] [--player_2 PLAYER_2]
                    [--board_size BOARD_SIZE] [--display]
                    [--display_delay DISPLAY_DELAY]

optional arguments:
  -h, --help            show this help message and exit
  --player_1 PLAYER_1
  --player_2 PLAYER_2
  --board_size BOARD_SIZE
  --display
  --display_delay DISPLAY_DELAY
  --autoplay
  --autoplay_runs AUTOPLAY_RUNS
```

## Issues? Bugs? Questions?

Feel free to open an issue in this repository, or contact us in Ed thread.

## About

This is a class project for COMP 424, McGill University, Fall 2023 (it was originally forked with the permission of Jackie Cheung).

## License

[MIT](LICENSE)
