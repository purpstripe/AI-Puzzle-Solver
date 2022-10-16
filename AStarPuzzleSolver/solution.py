import puzzle
import generator
import math
import csv
import time

class Node:
    """Node class for holding puzzle states and buildling the A* tree"""
    def __init__(self, puzzle, path_cost, parent = None):
        """Constructor for a Node"""
        self.puzzle = puzzle        # attribute to save the puzzle state
        self.path_cost = path_cost  # attribute to save the cost of the path (g(n))
        self.parent = parent        # attribute to point to each Node's parent

    def __str__(self):
        """Method for creating the string representation of a Node"""
        retStr = str(self.puzzle) + "\n"    # print the puzzle state of the Node
        retStr += "path cost: " + str(self.path_cost)   # print the path cost of the Node
        return retStr

    def get_f_value(self, heuristic):
        """Method for getting the f(n) value of a Node based on the function, heurisitc
            and the Node's path cost"""
        return self.path_cost + heuristic(self.puzzle)

def list_to_puzzle(lst):
    """Function for turning a one dimensional list into a two dimensional puzzle object"""
    puz_board = [] # list for storing the puzzle state
    list_len = len(lst) # variable to store the length of the input list
    # getting the size of the puzzle from the length of the list
    puz_dim = int(math.sqrt(list_len))
    # iterating through the rows of the puzzle
    for i in range(puz_dim):
        temp_list = []      # temporary list to store a single column
        # iterating through a column
        for j in range(puz_dim):
            # appending the list values to the puzzle state column
            temp_list.append(int(lst[j + (i * puz_dim)]))
        puz_board.append(temp_list) # appending the column list to the puzzle state list
    # creating a puzzle object based off of the puzzle state and size
    puz = puzzle.Puzzle(puz_dim, puz_board)
    # setting the location of the empty tile into the puzzle object
    puz.set_empty_tile(puz.find_empty_tile())
    # return the puzzle object instance
    return puz

def get_puzzles_from_config(file_name):
    """Function for creating a list of puzzle object instances from
        the config file"""
    puz_list = [] # list of puzzle instances
    # opening the file to read
    with open(file_name, 'r') as config:
        # csv reading object instance
        csv_reader = csv.reader(config)
        # iterating through every line in the opened file
        for line in csv_reader:
            # adding each new Puzzle object instance to the puzzle list
            puz_list.append(list_to_puzzle(line))
    # return the list of new Puzzles
    return puz_list

def heuristic_1(puzzle):
    """Function for computing the first heuristic, the number
        of misplaced tiles (not including the blank, 0)"""
    # variable for counting the number of misplaced tiles
    num_misplaced_tiles = 0
    # iterating through the whole puzzle
    for i in range(puzzle.puzzle_size):
        for j in range(puzzle.puzzle_size):
            # if the tile is not blank...
            if puzzle.get_tile(i, j) != 0:
                # if the tile is out of place - not equal to the sequential form
                # of the solution, 0 to puzzle size - 1
                if puzzle.get_tile(i, j) != (j + (i * puzzle.puzzle_size)):
                    # increment number of misplaced tiles
                    num_misplaced_tiles += 1
    # return the number of misplaced tiles, the val of this first heuristic
    return num_misplaced_tiles    

def get_correct_tile_loc(tile_num, puzzle_size):
    """Function that gets the correct location of a tile value
        based off of the location of tiles in the solution state"""
    row = tile_num // puzzle_size
    col = tile_num % puzzle_size
    return {"row": row, "column": col}

def heuristic_2(puzzle):
    """Function for calculating the second heuristic,
        the Manhattan distance of the given board state"""
    # variable for counting the Manhattan distance of the puzzle
    total_manhattan_dist = 0
    # iterating through all tiles of the puzzle
    for i in range(puzzle.puzzle_size):
        for j in range(puzzle.puzzle_size):
            # checking if the tile is empty - if so, ignore
            if puzzle.get_tile(i, j) != 0:
                # getting the correct location of a given tile 
                correct_loc = get_correct_tile_loc(puzzle.get_tile(i, j), puzzle.puzzle_size)
                # getting the difference between the correct location of tile and its current location
                col_dist = abs(correct_loc["column"] - j)
                row_dist = abs(correct_loc["row"] - i)
                # summing the Manhattan distances for each tile
                total_manhattan_dist += (col_dist + row_dist)
    # returning the total Manhattan distance
    return total_manhattan_dist

def heuristic_3(puzzle):
    """Function for calculating the third heuristic, the number
        of swaps used to sort a one dimensional version of the
        puzzle state with maxsort"""
    # converting the puzzle to a one dimensional list
    one_dim_puzzle = puzzle.get_one_dim_puzzle()
    # counting the number of swaps used to sort
    num_swaps = 0
    # iterating through the puzzle list backwards
    for i in range( (len(one_dim_puzzle) - 1), 0, -1):
        # keeping track of the max value in the list or sublist being sorted
        max = 0
        # iterating through the part of the list being considered
        for j in range(1, i+1):
            # checking if there's a new max value in the list/sublist
            if one_dim_puzzle[max] < one_dim_puzzle[j]:
                max = j     # set new max
        # making sure the swap is necessary
        if one_dim_puzzle[i] != one_dim_puzzle[max]:
            # swap element and max element of the puzzle list/sublist
            one_dim_puzzle[i], one_dim_puzzle[max] = one_dim_puzzle[max], one_dim_puzzle[i]
            # incremenet the number of swaps
            num_swaps += 1
    # return the number of swaps
    return num_swaps

def heuristic_4(puzzle):
    """Function for calculating the fourth heuristic, the sum of Euclidean distance of 
        each tile in its current location to its correct location"""
    # variable to keep track of the total Euclidean distance of all tiles
    total_euclid_dist = 0
    # iterating through all of the tiles in the puzzle state
    for i in range(puzzle.puzzle_size):
        for j in range(puzzle.puzzle_size):
            # ignoring the blank space/empty tile
            if puzzle.get_tile(i, j) != 0:
                # calculating the correct location of the current tile at i,j
                correct_loc = get_correct_tile_loc(puzzle.get_tile(i, j), puzzle.puzzle_size)
                # getting the square of the row and column distance of the current tile
                # location to the correct tile location
                square_col_dist = (correct_loc["column"] - j) ** 2
                square_row_dist = (correct_loc["row"] - i) ** 2
                # summing the square root of the squared row and column distances
                total_euclid_dist += math.sqrt(square_col_dist + square_row_dist)
    # return the total Euclidean distance
    return total_euclid_dist
    

class PriorityQueueHeap:
    """Class for implementing the frontier of the A* algorithm as a 
        binary heap based priority queue"""
    
    def __init__(self, heuristic):
        """Constructor for the priority queue"""
        # elements list to be populated with A* Nodes
        self.elements = []
        # keeping track of the size of the queue
        self.size = 0 
        # given heuristic used to evaluate each A* Node
        self.heuristic = heuristic
        
    def swap(self, i , j):
        """Function for swapping queue elements"""
        self.elements[i], self.elements[j] = self.elements[j], self.elements[i]

    def parent(self, index):
        """Function for getting the index of a parent Node based
            off of the index of the current Node. An indexed list
            is used to hold all of the A* Nodes"""
        return (index - 1) // 2

    def left_child(self, index):
        """Function for getting the index of the left child Node
        based off of the index of the current Node. An indexed list
        is used to hold all of the A* Nodes"""
        return ((2 * index) + 1)

    def right_child(self, index):
        """Function for getting the index of the right child Node
            based off of the index of the current Node. An indexed list
            is used to hold all of the A* Nodes"""
        return ((2 * index) + 2)

    def is_empty(self):
        """Function that checks if the priority queue is empty"""
        return self.size == 0 

    def bubble_up(self, index):
        """Function for bubbling up Nodes into their proper position in the heap
            based off the the f(n) value calculated from the g(n), path cost, and the
            h(n), heuristic"""
        # getting the f value of the parent Node
        parent_val = self.elements[self.parent(index)].get_f_value(self.heuristic)
        # getting the f value of the current Node
        current_val = self.elements[index].get_f_value(self.heuristic)

        # while the Node is not at the root and has an f value smaller than the parent...
        while index > 0 and parent_val > current_val:
            # swap Node with the parent
            self.swap( self.parent(index), index )
            # set the Node's new index
            index = self.parent(index)

    def bubble_down(self, index):
        """Function for bubbling down Nodes into their proper position in the heap
            based off the f(n) value calculated from the g(n), path cost, and the 
            h(n), heuristic"""
        # setting the assumed min index
        min_index = index
        # getting the f value of the min index
        min_val = self.elements[min_index].get_f_value(self.heuristic)

        # getting the index of the left child
        left_index = self.left_child(index)
        # if the left child is in the queue
        if left_index < self.size:
            # get the f value of the left child
            left_val = self.elements[left_index].get_f_value(self.heuristic)
            # if the f value of the left child is smaller than the current min
            if left_val < min_val:
                # set the new min index
                min_index = left_index 
                # recalculate the min f value
                min_val = self.elements[min_index].get_f_value(self.heuristic)

        # get the index of the right child
        right_index = self.right_child(index)
        # check if the right child is in the queue
        if right_index < self.size:
            # if so, calculate the f value of the right child Node
            right_val = self.elements[right_index].get_f_value(self.heuristic)
            # if the f value of the right child is less than the min f value...
            if right_val < min_val:
                # reset the min index to the correct value
                min_index = right_index
                # and recalculate the min f value
                min_val = self.elements[min_index].get_f_value(self.heuristic)

        # if the min index was changed
        if index != min_index:
            # swap the current index with the child with the minimum f value
            self.swap(index, min_index)
            # recur bubble down with the swapped Node - larger f value and lower priority 
            self.bubble_down(min_index)

    def push(self, node):
        """Function for pushing a Node into the correct position of the heap
            and priority queue"""
        # increment the size of the queue
        self.size += 1
        # add the Node to the underlying list of the queue
        self.elements.append(node)
        # bubble up the new value into its correct location
        self.bubble_up(self.size - 1)

    def pop(self):
        """Function for popping the Node with the highest priority (lowest f(n))"""
        # save the first Node - highest priority
        pop_node = self.elements[0]

        # set the top Node to the last element in the list/queue
        self.elements[0] = self.elements[self.size - 1]
        # remove the last element in the list
        self.elements = self.elements[:-1]
        # reduce the size of the queue by 1
        self.size -= 1

        # if there are left and right children...
        if self.size > 3:
            # bubble down the node at the top of the heap
            self.bubble_down(0)
        # return the saved popped Node
        return pop_node


"""
def get_min_node_from_frontier(node_list, heuristic):
#    Function for getting the Node with the puzzle state with the 
 #       minimum f(n) value from a list of Nodes based on its path cost 
  #      (g(n)) and the heuristic function (h(n))
    min_node = node_list[0]     # assume first Node has the min state 
    min_f = min_node.get_f_value(heuristic)     # getting the first Node's f value
    # iterating through the rest of the list (without the first val)
    for node in node_list[1:]:
        # checking for a new Node with a new minimum f value
        if node.get_f_value(heuristic) < min_f:
            min_node = node     # setting a new min node
            # setting the new minimum f value
            min_f = node.get_f_value(heuristic)
    # returning the Node with the minimum state
    return min_node
"""


def expand(parent_node):
    """Function that returns a list of children Nodes of the parent
        Node arugment by generating neighboring puzzle states from the
        parent Node's puzzle state and creating Node instances with these states"""
    puzzle = parent_node.puzzle     # getting the parent Node's puzzle state
    child_nodes = []        # creating a list for child Nodes
    # generating a list of neighboring puzzle states from the parent's puzzle state
    neighbor_puzzles = puzzle.generate_puzzle_neighbors()
    # iterating through the neighboring puzzle states
    for puz in neighbor_puzzles:
        # calculating the path cost for the new Node
        cost = parent_node.path_cost + 1
        # adding a new Node instance to the list of child Nodes
        child_nodes.append(Node(puz, cost, parent_node))
    # returning the list of child Nodes
    return child_nodes

def puzzle_to_tuple(puz):
    """Turns a puzzle list into a tuple for use as a 
        dictionary key"""
    return tuple(map(tuple, puz.puzzle))

def a_star(init_puzzle, heuristic):
    """Function implementation of A*"""
    print("initial state")
    # printing the initial state of the puzzle
    print(init_puzzle)
    # variable to keep track of the number of Nodes considered by A*
    num_nodes = 0
    # variable for the start time of the A* function
    start = time.perf_counter()
    # creating a root Node for the search tree
    root_node = Node(init_puzzle, 0)
    # populate the frontier with the root Node
    frontier = PriorityQueueHeap(heuristic) 
    frontier.push(root_node)
    num_nodes += 1   # the root node is put in the frontier
    # populate the reached list with the root
    reached = {puzzle_to_tuple(init_puzzle): root_node}
    # while the frontier is not empty
    while not frontier.is_empty():
        # get the Node with the minimum state from frontier
        # based on its path cost and the heuristic function
        min_node = frontier.pop()
        # if the Node has the goal state, return the Node
        if min_node.puzzle.is_puzzle_solved():
            # variable for the time of the end of A*
            end = time.perf_counter()
            print()
            print("final state")
            # printing the completed puzzle
            print(min_node.puzzle)
            # print the total number of Nodes considered by A*
            print("total number of Nodes added to the frontier: " + str(num_nodes))
            # print the time taken by the A* function
            print("time to finish: " + str(end - start))
            return (min_node, num_nodes)
        # for each child Node of the Node with minimum state...
        for child in expand(min_node):
            # variable for the current child's puzzle state
            child_puz = child.puzzle
            # if the puzzle state is not a Node in the reached list, add it to reached
            # if the current child Node has a better path cost than another Node
            # in reached with the same puzzle state, update this Node in reached 
            # with the child Node
            # push the child to frontier
            child_tuple = puzzle_to_tuple(child_puz)
            if not child_tuple in reached or (child.path_cost < reached[child_tuple].path_cost):
                reached[child_tuple] = child
                frontier.push(child)
                # increment number of nodes added to frontier
                num_nodes += 1
    # the A* search failed
    print("search failed")


"""
def a_star(init_puzzle, heuristic):
    #Function implementation of A*
    print("initial state")
    # printing the initial state of the puzzle
    print(init_puzzle)
    # variable to keep track of the number of Nodes considered by A*
    num_nodes = 0
    # variable for the start time of the A* function
    start = time.perf_counter()
    # creating a root Node for the search tree
    root_node = Node(init_puzzle, 0)
    # populate the frontier with the root Node
    frontier = [root_node]
    num_nodes += 1   # the root node is put in the frontier
    # populate the reached list with the root
    reached = {puzzle_to_tuple(init_puzzle): root_node}
    # while the frontier is not empty
    while frontier:
        # get the Node with the minimum state from frontier
        # based on its path cost and the heuristic function
        min_node = get_min_node_from_frontier(frontier, heuristic)
        # remove that Node from the frontier
        frontier.remove(min_node)
        # if the Node has the goal state, return the Node
        if min_node.puzzle.is_puzzle_solved():
            # variable for the time of the end of A*
            end = time.perf_counter()
            print()
            print("final state")
            # printing the completed puzzle
            print(min_node.puzzle)
            # print the total number of Nodes considered by A*
            print("total number of Nodes added to the frontier: " + str(num_nodes))
            # print the time taken by the A* function
            print("time to finish: " + str(end - start))
            return min_node
        # for each child Node of the Node with minimum state...
        for child in expand(min_node):
            # variable for the current child's puzzle state
            child_puz = child.puzzle
            # if the puzzle state is not a Node in the reached list, add it to reached
            # and add it to the frontier
            # if the current child Node has a better path cost than another Node
            # in reached with the same puzzle state, update this Node in reached 
            # with the child Node
            # append the child to frontier
            child_tuple = puzzle_to_tuple(child_puz)
            if not child_tuple in reached or (child.path_cost < reached[child_tuple].path_cost):
                reached[child_tuple] = child
                frontier.append(child)
                # increment number of nodes added to frontier
                num_nodes += 1
    # the A* search failed
    print("search failed")
"""