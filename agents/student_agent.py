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

    #if chess_board[my_r, my_c, student_agent.dir_map["u"]] and chess_board[my_r, my_c, student_agent.dir_map["u"]]

    return 0.5*student_agent.heuristic_factor#TODO


def g(student_agent):
    return student_agent.num_steps_taken

def f(student_agent, chess_board, my_pos, adv_pos):
    return g(student_agent) + h(student_agent, chess_board, my_pos, adv_pos)

#TODO could rewrite h, g, f to be functions inside student agent class


def getAllNeighboringGameStates(chess_board, my_pos, adv_pos):
    #TODO return list of neighboring game states (extactly 1 hop away) -> moving up, down, left, or right, PLUS putting wall down u,d,l,r for each possible movement -> 4*4=16 total possible neighboring game states
   
    neighbors = [] # list of 3 tuples
    
    #len(neighbors) will probably be less than 16 because we cant put walls if there are already some there and cant move if a wall or opponent is in the way
    # TODO implement    
    assert len(neighbors)<=16, "Max of 16 neighboring game states"
    return neighbors


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

        #TODO 
        #need to try every possible sequence of hops < max_step, while keeping track of lowest f(n)
        
        #need to call f(self, chess_board, my_pos, adv_pos)
        #TODO  pick move that has the lowest f(n)
        


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
        
        example: when numHops = 0 -> no hops are done so we have 4 options of where to put wall (u,d,l,r), call f(n) for each of the 4 wall placement and keep track of smallest f(n) 
        when max_step = 1 -> try numHops =0, follow instruction above. Then try numHops = 1. Hopping 1 time gives us 4 possible options: going up, down, left, or right. For each of these 4 moves, we have 4 options of wall placement (u,d,l,r). So for 1 numHop we have 4*4=16 total options without counting options of 0 numHops
        --------------------------------
        
        
        """
        print("--------------------------------------------------------")
        
        # Perform depth-limited BFS on graph of game state nodes starting at current game state
        # max depth = max_step (unless there are time/memory requirements to meet)
        BFS_MAX_DEPTH = max_step 
        queue = Queue() # put() to enqueue and get() to dequeue
        queue.put(((chess_board, my_pos, adv_pos), 0)) # enqueue starting (current) game state + starting depth
        # queue contains tuple: (game state, depth/numHops)
        # game state is 3 tuple: (chess_board, my_pos, adv_pos)
        visitedNodes = set()
        visitedNodes.add((chess_board, my_pos, adv_pos)) # mark starting state as visited
        while not queue.empty():
            # removing game state from queue and visiting its neighbours
            bfs_game_state, bfs_depth = queue.get()
            bfs_chess_board, bfs_my_pos, bfs_adv_pos = bfs_game_state


            #TODO GET F(BFS_GAME_STATE) = g + h AND KEEP TRACK OF LOWEST ONE HERE and game state
            
            if bfs_depth < BFS_MAX_DEPTH:
                for neighbor in getAllNeighboringGameStates(bfs_chess_board, bfs_my_pos, bfs_adv_pos):#all direct neighbours (1 hop away) of the game state
                    if neighbor not in visitedNodes:
                        queue.put((neighbor, bfs_depth+1))
                        visitedNodes.add(neighbor)
            
        print("---------------------------------------------------------")


        
        time_taken = time.time() - start_time
        
        print("Victor's AI's turn took ", time_taken, "seconds.")
        #print(">>>>>>>>>>>>>>>>>>>>>>>>"+str(max_step))
        #print(">>>>>>>>>>>>>"+str(chess_board[0,0, self.dir_map["l"]]))

        self.num_steps_taken += 1#step function was called, so increment by one
        

        # dummy return
        return my_pos, self.dir_map["u"]
