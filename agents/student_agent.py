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

game state is a 3-tuple: chess_board, my_pos, adv_pos

BFS

"""

# h is the heuristic function
# chess_board is to know where the walls are
# my_pos and adv_pos to determine where players are on board
# need to return a low number when game state is good for my player
# need to return a high number when game state is bad for my player
# returns a 0% if this game state is a winning game state for this player (game over)
# returns a 100% if this game state is a losing game state for this player (game over)
# returns a number between 0% and 100% of the heuristic_factor
# heuristic_factor is to scale range of values returned by h(n)
def h(student_agent, chess_board, my_pos, adv_pos):
    my_r, my_c = my_pos
    #chess_board True means wall
    #if chess_board[my_r, my_c, student_agent.dir_map["u"]] and chess_board[my_r, my_c, student_agent.dir_map["u"]]


    return 0.5*student_agent.heuristic_factor#TODO


def g(student_agent):
    return student_agent.num_steps_taken

def f(student_agent, chess_board, my_pos, adv_pos, wall_dir):
    #returns f val IF we add a wall at chess_board[r][c][wall_dir]
    r, c = my_pos
    chess_board[r][c][wall_dir] = True
    return g(student_agent) + h(student_agent, chess_board, my_pos, adv_pos)

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
        self.heuristic_factor = 100 #to scale range of values returned by h(n)    

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
        print("--------------------------------------------------------")
        
        # Perform depth-limited BFS on graph of game state nodes starting at current game state
        # max depth = max_step (unless there are time/memory requirements to meet)
        BFS_MAX_DEPTH = max_step 
        queue = Queue() # put() to enqueue and get() to dequeue
    
        # chess_board and adv_pos dont need to be added to queue or visitedNodes since they dont change in this iteration of the step func
        queue.put((my_pos, 0))# enqueue starting (current) position + starting depth

        # queue contains tuple: (new_pos, depth/numHops)
        visitedNodes = set() # to prevent cycles
        visitedNodes.add(my_pos) # keeps track of which positions we tried 

        print("Starting position: "+str(my_pos)) 
        
        best_new_pos = (0,0) #dummy val
        best_wall_dir = 0 #dummy val
        best_f = self.heuristic_factor #dummy val
        
        while not queue.empty():
            bfs_pos, bfs_depth = queue.get()

            # try adding wall at each 4 location when my_pos = bfs_pos and keep track of smallest f(n)
            
            r, c = bfs_pos
            for wall_dir in range(4):
                if not chess_board[r][c][wall_dir]: #cant put wall down if there already is one
                    x = f(self, chess_board, bfs_pos, adv_pos, wall_dir)
                    print("F score: "+str(x))
                    if x<=best_f:
                        best_f = x
                        best_wall_dir = wall_dir
                        best_new_pos = bfs_pos
            
            #print("Position "+str(bfs_pos)+" at depth "+str(bfs_depth))
            if bfs_depth < BFS_MAX_DEPTH:
                for neighbor in getAllPossiblePositionsOneHopAway(chess_board, bfs_pos, adv_pos):
                    if neighbor not in visitedNodes:
                        queue.put((neighbor, bfs_depth+1))
                        visitedNodes.add(neighbor)
            
        print("---------------------------------------------------------")


        
        time_taken = time.time() - start_time
        
        print("Victor's AI's turn took ", time_taken, "seconds.")
        #print(">>>>>>>>>>>>>>>>>>>>>>>>"+str(max_step))
        #print(">>>>>>>>>>>>>"+str(chess_board[0,0, self.dir_map["l"]]))

        self.num_steps_taken += 1#step function was called, so increment by one
    
        return best_new_pos, best_wall_dir
