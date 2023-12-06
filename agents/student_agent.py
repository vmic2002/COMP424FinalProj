# Student agent: Add your own agent here
from agents.agent import Agent
from store import register_agent
import sys
import numpy as np
from copy import deepcopy
import time
from queue import Queue

"""
We have chosen to implement a heuristic search similar to A* without guarenteeing that h is optimal

we want to minimize f(n) = g(n) + h(n) to find shortest path in graph of game states
g(n) -> self.num_steps_taken
h(n) is defined below

TODO ITS POSSIBLE WE ARE DOING GREEDY HEURISTIC ONLY SEARCH SINCE G(N) IS THE SAME THROGUH EVERY ITERATION OF STEP FUNC

game state is a 3-tuple: chess_board, my_pos, adv_pos

BFS

"""

# h is the heuristic function
# chess_board is to know where the walls are
# my_pos and adv_pos to determine where players are on board
# need to return a low number when game state is good for my player
# need to return a high number when game state is bad for my player
# returns a low number if this game state is a winning game state for this player (game over)
# returns a high number if this game state is a losing game state for this player (game over)
# h = c1 * var1 + c2 * var2 + c3 * var3 + ...
# could maybe use least squares line of best fit method to find the best scalors c1, c2 ...

def h(student_agent, chess_board, new_pos, adv_pos, wall_dir, starting_pos):
    new_r, new_c = new_pos
    adv_r, adv_c = adv_pos
   
    # Calculate the game phase 
    # estimate if we are early or late in the game and change heurisitic scalors
    total_turns_in_match = chess_board.shape[0] * chess_board.shape[1]  #TODO estimate how early/late we are in match using numWalls or student_agent.num_steps_taken
    turns_played = student_agent.num_steps_taken
    game_phase = 'late' if turns_played > total_turns_in_match / 2 else 'early'
    
    # NOTE: These constants resulted in 100% victory.
    # Set weights dynamically based on the game phase
    if game_phase == 'early':
        # Early game: prioritize exploration and control
        c1, c2, c3, c4 = 1, 5, -0.5 ,20
    else:
        # Late game: prioritize securing space and trapping the opponent
        c1, c2, c3,c4 = 1, 10, -1 , 50  

    #in this func AGENT IS AT STARTING_POS
    #THIS H CALL IS TO DECIDE IF MOVING TO NEW_POS AND ADDING A WALL AT WALL_DIR A GOOD DECISION
    #IF IT IS RETURN SMALL NUMBER ELSE BIG NUMBEr
    #chess_board contains this added wall (it is removed at end of f function call) 
        
    #chess_board True means wall
    #if chess_board[my_r, my_c, student_agent.dir_map["u"]] and chess_board[my_r, my_c, student_agent.dir_map["u"]]
    
    # h = c1 * my_r + c2 * my_c + c3 * otherVariable + ...
    # could maybe use least squares line of best fit method to find the best constants c1, c2 ...
    # no more heuristic_factor -> dont need to scale h, negative values work too (negative means game state is super favored)
        
    #for now trying linear combination, could potentially try other functions
    
    # Distance Between Players
    distanceBetweenMeAndAdv = abs(new_r-adv_r)+abs(new_c-adv_c)
    
    # Board Control and Division
    num_squares_accessible = flood_fill(chess_board, new_pos)
    c3 = -0.5  # Negative weight, as more controlled area is better
    
    # Check if the agent is surrounded by three walls
    wall_count = sum(chess_board[new_r, new_c])
    trapped_penalty = c4 * (1 if wall_count >= 3 else 0)


    # -------IMPORTANT-------------
    #variables used for h should be vars that change within the step function. numWalls and adv_pos dont change
    # new_pos and where the wall was just added (so chess_board and wall_dir) are the only things that will change within the step function
    # !!!!!!!!!!!!!
    # h estimates if adding a wall at new_pos in wall_dir is a good idea if we are currently at starting_pos
    # !!!!!!!!!!!!!!
    # --->   h(new_pos, wall_dir, chess_board), numWalls, adv_pos... are constants in this function so we can just leave them out
    # ----------------------------
    
    return c1*distanceBetweenMeAndAdv + c3*num_squares_accessible + c4*trapped_penalty

def flood_fill(chess_board, start_pos):
    """
    Performs a flood-fill algorithm to count the number of accessible squares from a given starting position.
    
    Parameters:
    chess_board (array): A 3D array representing the game board with walls.
    start_pos (tuple): The starting position (row, column) for the flood-fill.
    
    Returns:
    int: The number of squares accessible from the start_pos.
    """

    # Determine the size of the chessboard 
    M = chess_board.shape[0]

    # Initialize a set to track visited squares to avoid re-visiting
    visited = set()

    # Use a queue to manage the positions to explore next, starting with start_pos
    queue = [start_pos]

    # Mapping from direction strings to their indices in the chess_board array
    # This helps in determining the presence of walls in each direction
    dir_map = {"u": 0, "r": 1, "d": 2, "l": 3}

    # The moves associated with each direction
    # Used to calculate the coordinates of adjacent squares
    moves = ((-1, 0), (0, 1), (1, 0), (0, -1))

    # Main loop to explore each square in the queue
    while queue:
        # Pop the first position from the queue
        r, c = queue.pop(0)

        # Skip if already visited to prevent redundant checks
        if (r, c) in visited:
            continue
        
        # Mark the current square as visited
        visited.add((r, c))

        # Check each direction from the current square
        for dir_index, (dr, dc) in zip(dir_map.values(), moves):
            # Calculate the coordinates of the adjacent square
            nr, nc = r + dr, c + dc

            # Check if the adjacent square is within bounds and accessible
            # It must not be blocked by a wall and should not be already visited
            if 0 <= nr < M and 0 <= nc < M and not chess_board[r, c, dir_index] and (nr, nc) not in visited:
                # If accessible, add it to the queue for further exploration
                queue.append((nr, nc))

    # Return the number of unique accessible squares found from start_pos
    return len(visited)



def numWalls(chess_board):
    #CORRECT! return number of walls on board without counting the walls around the edges of chess_board
    num_walls=0
    #this approach doesnt really work because there are duplicate counts in the 
    for r in range(len(chess_board)):
        for c in range(len(chess_board[r])):
            for wall_dir in range(len(chess_board[r][c])):
                if chess_board[r][c][wall_dir]: #chess_board True means wall
                    num_walls+=1
    numWallsAroundEdges=2*len(chess_board)+2*len(chess_board[0])#there are walls around edges of board but we dont want to count them
    #num_walls contains double counted walls (walls not on edges of chess_board)
    #numWallsAroundEdges arent double counted in num_walls
    return int((num_walls-numWallsAroundEdges)/2)#all walls are double counted in chess_board, right wall at r,c is counted again as left wall at r, c+1


def g(student_agent):
    return student_agent.num_steps_taken

def f(student_agent, chess_board, my_pos, adv_pos, wall_dir, starting_pos):
    #returns f val IF we add a wall at chess_board[r][c][wall_dir]
    # simulate adding wall at r,c, wall_dir and see what f is then remove wall
    r, c = my_pos
    #walls in middle of chessboard are double counted in chess_board, so need to set two values to True to simulate adding 1 wall
    #then set same two values back to False to remove that wall
    chess_board[r][c][wall_dir] = True
    if wall_dir == student_agent.dir_map["u"]:
        chess_board[r-1][c][student_agent.dir_map["d"]] = True
    elif wall_dir == student_agent.dir_map["d"]:
        chess_board[r+1][c][student_agent.dir_map["u"]] = True
    elif wall_dir == student_agent.dir_map["l"]:
        chess_board[r][c-1][student_agent.dir_map["r"]] = True
    elif wall_dir == student_agent.dir_map["r"]:
        chess_board[r][c+1][student_agent.dir_map["l"]] = True

    f_cost = h(student_agent, chess_board, my_pos, adv_pos, wall_dir, starting_pos) # TODO COULD USE G AS WELL+ g(student_agent) 
    chess_board[r][c][wall_dir] = False #numpy arrays are passed by reference so dont want to actually add wall  
    if wall_dir == student_agent.dir_map["u"]:
        chess_board[r-1][c][student_agent.dir_map["d"]] = False
    elif wall_dir == student_agent.dir_map["d"]:
        chess_board[r+1][c][student_agent.dir_map["u"]] = False
    elif wall_dir == student_agent.dir_map["l"]:
        chess_board[r][c-1][student_agent.dir_map["r"]] = False
    elif wall_dir == student_agent.dir_map["r"]:
        chess_board[r][c+1][student_agent.dir_map["l"]] = False
    return f_cost

#TODO could rewrite h, g, f to be functions inside student agent class


def getAllPossiblePositionsOneHopAway(chess_board, my_pos, adv_pos):
    # RETURN ALL POSSIBLE MY_POS BY MAKING ONE HOP, DONT CARE ABOUT ADDING WALL, need to be careful not to bump in adversary or wall
    # need to return list of (r, c) like my_pos, max length 4
    # code copied from random_agent.py
    # Moves (Up, Right, Down, Left)
    moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
    
    r, c = my_pos
 
    # Build a list of the moves we can make
    allowed_dirs = [ d
      for d in range(0,4)                           # 4 moves possible
      if not chess_board[r,c,d] and                 # chess_board True means wall
      not adv_pos == (r+moves[d][0],c+moves[d][1])] # cannot move through Adversary
    
    
    positions = []
    for d in allowed_dirs:
        m_r, m_c = moves[d]
        positions.append((r + m_r, c + m_c))

    #for p in positions:
    #    print("PPPPP:  "+str(p))
    return positions



@register_agent("student_agent")
class StudentAgent(Agent):
    """
    A dummy class for your implementation. Feel free to use this class to
    add any helper functionalities needed for your agent.
    """

    def __init__(self):
        super(StudentAgent, self).__init__()
        self.name = "StudentAgent"
        self.dir_map = {
            "u": 0,
            "r": 1,
            "d": 2,
            "l": 3,
        }
        self.num_steps_taken = 0 #num times step function is called, to determine g(n)
       # self.heuristic_factor = 100 #to scale range of values returned by h(n)    

    def step(self, chess_board, my_pos, adv_pos, max_step):
        """
        Implement the step function of your agent here.
        You can use the following variables to access the chess board:
        - chess_board: a numpy array of shape (x_max, y_max, 4)
            (_ , _, self.dir_map["u"]) or self.dir_map["l"]...
            chess_board(_, _, _) = True means wall (there are walls on the borders so agents dont go off-screen)
        - my_pos: a tuple of (x, y)
        - adv_pos: a tuple of (x, y)
        - max_step: an integer

        You should return a tuple of ((x, y), dir),
        where (x, y) is the next position of your agent and dir is the direction of the wall
        you want to put on.

        Please check the sample implementation in agents/random_agent.py or agents/human_agent.py for more details.
        """

        # Some simple code to help you with timing. Consider checking 
        # time_taken during your search and breaking with the best answer
        # so far when it nears 2 seconds.
        start_time = time.time()

         
        #need to try every possible sequence of hops < max_step, while keeping track of lowest f(n)
        
        #  pick move that has the lowest f(n)
        


        """
        need to try every possible sequence of hops < max_step
        for example if max_step = 3, need to check all possible moves for doing 0, 1, 2, and 3 hops
        num hops taken <= max_step 
        num hops taken  : max  num possible moves (without counting walls to put down)
        0 : 1 -> 0 hops taken means only 1 possible move (dont move)
        0,1 : 5  -> making 0 hop then 1 hop, 5 total move options (u, d, l, r, no movement)
        0,1,2 : 13
        0,1,2,3 : 25
        0,1,2,3,4 : 41
        0,1,2,3,4,5 : 61 -> for num hops = 0, 1, 2, 3, 4, then 5, 61 total move options (r,c) to go to
        ...
       
         
        0,1 : 2(2)+1  # +1 for no movement
        0,1,2 : 2(4)+2(2)+1
        0,1,2,3 : 2(6)+2(4)+2(2)+1
        0,1,2,3,4 : 2(8)+2(6)+2(4)+2(2)+1
        0,1,2,3,4,5 : 2(10)+2(8)+2(6)+2(4)+2(2)+1
                                

        0,1,...,max_step : 4*(1+2+3+...+max_step)+1


         
        # total number of moves counting wall to put down <= max num possible moves (without putting wall down) * 4 (biggest case have 4 options to put wall down: u,d,l,r)
        total num moves when trying 0 hop, 1 hop, ..., max_step hops and placing a wall = 4*(4*(1+2+3+...+max_step)+1)
        
        = 4*(4*(max_step*(max_step+1)/2)+1)
        = 4*(2*max_step*(max_step+1)+1)
        = 8*max_step*(max_step+1)+4
        = O(max_step^2)
        
        for each move, we need to get f(n) and keep track of lowest ones (break tie with randomness)
        
        for max_step = 5, total number of moves (including putting wall down) = 61*4=244    

    
        ---------pseudocode------------
        need to try hopping numHops=0...max_step inclusive. THIS IS BFS -> numHops == depth in BFS graph from start
        for each numHops gather f(n) of each gamestate (adding walls u,d,l,r if possible)
        keep track of lowest f(n), what r and c, and where to put wall u or d or l or r
        
        We are traversing the graph as a "simulation" since we arent really performing the moves, we are traversing to find best possible move and pick that node

        example: when numHops = 0 -> no hops are done so we have 4 options of where to put wall (u,d,l,r), call f(n) for each of the 4 wall placement and keep track of smallest f(n) 
        when max_step = 1 -> try numHops =0, follow instruction above. Then try numHops = 1. Hopping 1 time gives us 4 possible options: going up, down, left, or right. For each of these 4 moves, we have 4 options of wall placement (u,d,l,r). So for 1 numHop we have 4*4=16 total options without counting options of 0 numHops
        --------------------------------
        
        
        """
        #print("--------------------------------------------------------")
        #print("Max step: "+str(max_step))        
        # Perform depth-limited BFS on graph of game state nodes starting at current game state
        # max depth = max_step (unless there are time/memory requirements to meet)
        BFS_MAX_DEPTH = max_step 
        queue = Queue() # put() to enqueue and get() to dequeue
    
        # chess_board and adv_pos dont need to be added to queue or visitedNodes since they dont change in this iteration of the step func
        queue.put((my_pos, 0))# enqueue starting (current) position + starting depth

        # queue contains tuple: (new_pos, depth/numHops)
        visitedNodes = set() # to prevent cycles
        visitedNodes.add(my_pos) # keeps track of which positions we tried 

        #print("Starting position: "+str(my_pos)) 
        
        best_new_pos = (0,0) #dummy val
        best_wall_dir = 0 #dummy val
        best_f = 10000000000 #dummy val
        
        while not queue.empty():
            bfs_pos, bfs_depth = queue.get()

            # try adding wall at each 4 location when my_pos = bfs_pos and keep track of smallest f(n)
             
            r, c = bfs_pos
            for wall_dir in range(0,4):
                if not chess_board[r][c][wall_dir]: #cant put wall down if there already is one
                    x = f(self, chess_board, bfs_pos, adv_pos, wall_dir, my_pos) # x is heursitic IF we place a wall at wall_dir
                    #print("F score: "+str(x)+" bfs_pos: "+str(bfs_pos)+ " wall_dir: "+str(wall_dir))
                    if x<=best_f:
                        #print("\tF score smaller than best_f: "+str(x))
                        best_f = x
                        best_wall_dir = wall_dir
                        best_new_pos = bfs_pos
            
            #print("Position "+str(bfs_pos)+" at depth "+str(bfs_depth))
            if bfs_depth < BFS_MAX_DEPTH:
                for neighbor in getAllPossiblePositionsOneHopAway(chess_board, bfs_pos, adv_pos):
                    if neighbor not in visitedNodes:
                        #print("adding neighbord at depth "+str(bfs_depth+1))
                        queue.put((neighbor, bfs_depth+1))
                        visitedNodes.add(neighbor)
            
        #print("---------------------------------------------------------")


        
        time_taken = time.time() - start_time
        
        #print("Victor's AI's turn took ", time_taken, "seconds.")
        #print(">>>>>>>>>>>>>>>>>>>>>>>>"+str(max_step))
        #print(">>>>>>>>>>>>>"+str(chess_board[0,0, self.dir_map["l"]]))

        self.num_steps_taken += 1#step function was called, so increment by one
    
        return best_new_pos, best_wall_dir
