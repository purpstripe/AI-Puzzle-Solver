import puzzle
import random
import csv

rand_seed = 0       # global seed variable - change this to generate new puzzles!

def generate_move_list(puz_size):
    """Generates a list of puzzle shuffle moves using integers 0-3"""
    global rand_seed    # use a seed for the random function
    move_list = []
    # iterate through the list generating numbers
    for i in range(puz_size):
        random.seed(rand_seed)  # seed function
        # add a random number between 0-3 inclusive
        move_list.append(random.randint(0, 3))
        rand_seed += 1  # increment random seed for next number
    return move_list    # return the shuffle move list

def shuffle_puzzle(puz):
    """Function for creating a shuffled puzzle based off of the puzzle argument"""
    # create a list of moves to shuffle the puzzle
    move_list = generate_move_list(puz.get_puzzle_size())
    # iterate through the numbers in a move list
    for num in move_list:
        # saving the location of the empty tile
        empty_tile_row = puz.empty_tile_loc["row"]
        empty_tile_column = puz.empty_tile_loc["column"]
        # checking the move direction and if it is possible
        # can we move the empty space up?
        if num == 0 and empty_tile_row > 0:
            # move the empty space up and update its location
            puz.swap_tiles(empty_tile_row, empty_tile_column, empty_tile_row - 1, empty_tile_column)
        # can we move the empty tile to the right?
        elif num == 1 and empty_tile_column < puz.puzzle_size - 1:
            # move the empty space to the right and update its location
            puz.swap_tiles(empty_tile_row, empty_tile_column, empty_tile_row, empty_tile_column + 1)
        # can we move the empty tile down?
        elif num == 2 and empty_tile_row < puz.puzzle_size - 1:
            # move the empty space down and update its location
            puz.swap_tiles(empty_tile_row, empty_tile_column, empty_tile_row + 1, empty_tile_column)
        # can we move the empty tile to the left?
        elif num == 3 and empty_tile_column > 0:
            # move the empty tile to the left and update its location
            puz.swap_tiles(empty_tile_row, empty_tile_column, empty_tile_row, empty_tile_column - 1)
    # return the shuffled puzzle
    return puz

def is_puzzle_unique(puz_list, new_puz):
    """Function to check if a puzzle state already exists in a list of puzzles"""
    # iterate through the puzzles in the list
    for puz in puz_list:
        # checking each puzzle for equalilty to the new_puz argument
        if new_puz.is_puzzle_equal(puz):
            # puzzle state exists in the list
            return False
    # puzzle is unique
    return True

def create_random_puz_list(puz_size, num_puzzles):
    """Function to create a number of random puzzles (num_puzzles)
        of a given size (puz_size) and puts them all in a list (puz_list)
        and returns this list of random puzzles"""
    # puzzle list
    puz_list = []
    # iterate the number of puzzles to create
    for i in range(num_puzzles):
        new_puzzle = puzzle.Puzzle(puz_size)    # new puzzle object
        new_puzzle.set_solution_puzzle()        # set puzzle to solution state
        puzzle_unique = False           # assume the puzzle is not unique
        # repeat until the puzzle has all tiles out of place and until the puzzle is unique
        while not new_puzzle.are_tiles_out_of_place() or not puzzle_unique:
            # shuffle the puzzle state
            new_puzzle = shuffle_puzzle(new_puzzle)
            # check if the puzzle is unique
            puzzle_unique = is_puzzle_unique(puz_list, new_puzzle)
        # add the random puzzle to the puzzle list
        puz_list.append(new_puzzle)
    return puz_list     # return the list of random puzzles 

def create_random_big_puz_list(puz_size, num_puzzles):
    """Function to create a number of big random puzzles (num_puzzles)
        of a given size (puz_size) and puts them all in a list (puz_list)
        and returns this list of random puzzles
        This function does not require that all tiles need to be out of place
        and instead sets a limit for time performace constraints"""
    # puzzle list
    puz_list = []
    # iterate the number of puzzles to create
    for i in range(num_puzzles):
        new_puzzle = puzzle.Puzzle(puz_size)    # new puzzle object
        new_puzzle.set_solution_puzzle()        # set puzzle to solution state
        puzzle_unique = False           # assume the puzzle is not unique
        # repeat until the puzzle has 11 or more tiles out of place and until the puzzle is unique
        min_tiles_out_of_place = 11
        while (new_puzzle.num_tiles_out_of_place() < min_tiles_out_of_place) or not puzzle_unique:
            # shuffle the puzzle state
            new_puzzle = shuffle_puzzle(new_puzzle)
            # check if the puzzle is unique
            puzzle_unique = is_puzzle_unique(puz_list, new_puzzle)
        # add the random puzzle to the puzzle list
        puz_list.append(new_puzzle)
    return puz_list     # return the list of random puzzles 

def write_puzzles_to_file(puz_list, file_name):
    """Function to write the states of a list of puzzles to the config file"""
    # open the config file in write mode
    with open(file_name, "w") as config:
        # create csv writing object
        csv_writer = csv.writer(config, delimiter=",")
        # iterate through all of the puzzles in the puzzle list
        for puz in puz_list:
            # write the puzzle state as a one dimensional list
            csv_writer.writerow(puz.get_one_dim_puzzle())

def append_puzzles_to_file(puz_list, file_name):
    """Function to append the states of a list of puzzles to the config file"""
    # open the config file in append mode
    with open(file_name, "a") as config:
        # create the csv writer object
        csv_writer = csv.writer(config, delimiter=",")
        # iterate through all of the puzzles in the puzzle list
        for puz in puz_list:
            # append the puzzle state as a one dimensional list
            csv_writer.writerow(puz.get_one_dim_puzzle())

# create 5 random 2x2 puzzles
puz_list = create_random_puz_list(2, 5)
# write puzzles to the config file
write_puzzles_to_file(puz_list, "config_file.csv")
# create 20 random 3x3 puzzles
puz_list = create_random_puz_list(3, 20)
# append puzzles to the config file
append_puzzles_to_file(puz_list, "config_file.csv")
# create 20 random 4x4 puzzles that are partially shuffled
puz_list = create_random_big_puz_list(4, 20)
# append puzzles to the config file
append_puzzles_to_file(puz_list, "config_file.csv")
print("config file populated")