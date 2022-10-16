import copy

# Puzzle class for storing all needed to represent a puzzle state
# and for creating puzzle specific functionality
class Puzzle:

    def __init__(self, puzzle_size, tiles = [], empty_tile_loc = {}):
        """Constructor for a puzzle"""
        self.puzzle_size = puzzle_size  # number of rows or columns in square puzzle
        self.puzzle = tiles             # the puzzle state represented as a two dimensional list
        self.empty_tile_loc = empty_tile_loc # dictionary to save the row and column of the empty space

    def __str__(self):
        """String method for printing a puzzle"""
        temp_str = ""
        for i in range(self.puzzle_size):
            for j in range(self.puzzle_size):
                temp_str += str(self.puzzle[i][j]) + " " # column elements separated by space
            if i < self.puzzle_size - 1:
                temp_str += "\n"    # rows separated by a new line    
        return temp_str

    def get_puzzle(self):
        """Gets the puzzle state of a given puzzle object"""
        return self.puzzle

    def get_one_dim_puzzle(self):
        """Turns the two dimensional puzzle state into a one dimensional list"""
        puzzle_list = []
        # iterate through all puzzle state tile values
        for i in range(self.puzzle_size):
            for j in range(self.puzzle_size):
                puzzle_list.append(self.puzzle[i][j]) # append each puzzle element to a list
        return puzzle_list

    def get_empty_tile(self):
        """Returns the dictionary containing the row and column of the empty space"""
        return self.empty_tile_loc

    def set_empty_tile(self, tile_loc):
        """Method for setting the location of the empty tile
            Expects a dictionary"""
        self.empty_tile_loc = tile_loc

    def find_empty_tile(self):
        """Method for finding the location of the empty tile in the puzzle"""
        row = -1        # initializing the row varible
        column = -1     # initializing the column variable
        empty_tile_found = False    # have we found the empty space?
        # iterate through the puzzle state
        for i in range(self.puzzle_size):
            for j in range(self.puzzle_size):
                if self.puzzle[i][j] == 0:      # checking current tile to see if empty
                    # setting row and column of empty space
                    row = i
                    column = j
                    empty_tile_found = True     # empty tile found, break from inner loop
                    break
            if empty_tile_found:                # empty tile founf, break from outer loop
                break
        return {"row": row, "column": column}   # return the empty location as a dictionary

    def set_puzzle(self, tiles):
        """Function for setting a puzzle's state"""
        # iterate through the puzzle tiles
        for i in range(self.puzzle_size):
            for j in range(self.puzzle_size):
                # set the puzzle tile with the correspoinding value
                # from the tiles argument (2 dim list)
                self.puzzle[i][j] = tiles[i][j]
        # setting the puzzle's empty tile location
        self.empty_tile_loc = self.find_empty_tile()

    def get_tile(self, row, column):
        """Returns the tile at specified location"""
        return self.puzzle[row][column]

    def get_puzzle_size(self):
        """Returns the size of a side of the square puzzle"""
        return self.puzzle_size

    def swap_tiles(self, row_0, col_0, row_1, col_1):
        """Swaps two tiles in the puzzle state by row and column location"""
        # checking if the location of the empty tile needs updating
        if self.puzzle[row_0][col_0] == 0:
            self.empty_tile_loc["row"] = row_1
            self.empty_tile_loc["column"] = col_1
        elif self.puzzle[row_1][col_1] == 0:
            self.empty_tile_loc["row"] = row_0
            self.empty_tile_loc["column"] = col_0
        # swapping the tiles in the puzzle
        self.puzzle[row_0][col_0], self.puzzle[row_1][col_1] = self.puzzle[row_1][col_1], self.puzzle[row_0][col_0]

    def is_puzzle_equal(self, other_puz):
        """Method for testing equality between the current puzzle and another puzzle"""
        if self.puzzle_size != other_puz.puzzle_size:   # puzzles not equal if they are different sizes
            return False
        # iterate through the tiles in both puzzles
        for i in range(self.puzzle_size):
            for j in range(self.puzzle_size):
                # checking for inequality between the two puzzle's tiles
                if self.puzzle[i][j] != other_puz.puzzle[i][j]: 
                    return False        # puzzles are not equal
        return True                     # puzzles are equal

    def is_puzzle_solved(self):
        """Checking if the current puzzle is solved"""
        solved = True
        one_dim_puz = self.get_one_dim_puzzle()     # turn the puzzle into a one dim list
        # iterate through all values in the puzzle list
        for i in range(len(one_dim_puz) - 1):
            # if an earlier element is bigger than a later element... 
            if one_dim_puz[i] > one_dim_puz[i+1]:
                # return false - puzzle not solved
                solved = False
        # otherwise, return true
        return solved

    def set_solution_puzzle(self):
        """Sets the state of the current puzzle to be the solved state"""
        self.puzzle = []    # list to contain the puzzle state
        # iterating through the rows
        for i in range(self.puzzle_size):
            temp_list = []      # temp list for populating the puzzle
            # iterating through the columns
            for j in range(self.puzzle_size):
                # appendeding the correct value for the given location
                # appended values are sequential from 0 to puzzle size - 1
                temp_list.append(j + (i * self.puzzle_size))
            # add list for a single column to the puzzle
            self.puzzle.append(temp_list)
        # setting the location of the empty tile to be the first location in the puzzle
        self.empty_tile_loc = {"row": 0, "column": 0}

    def are_tiles_out_of_place(self):
        """Checks a given puzzle if every tile is not in its original position"""
        # iterate through all values of the current puzzle
        for i in range(self.puzzle_size):
            for j in range(self.puzzle_size):
                # checking current tile for its value
                # does it have the value of the tile that is supposed to be in that position?
                if self.puzzle[i][j] == (j + (i * self.puzzle_size)):
                    return False    # at least one tile is in place
        return True     # all tiles are out of place
    
    def num_tiles_out_of_place(self):
        """Checks a given puzzle for the number of tiles not in their original position"""
        # variable to count number of tiles out of place
        num = 0
        # iterate through all values of the current puzzle
        for i in range(self.puzzle_size):
            for j in range(self.puzzle_size):
                # checking current tile for its value
                # does it have the value of the tile that is supposed to be in that position?
                if self.puzzle[i][j] != (j + (i * self.puzzle_size)):
                    num += 1    # tile out of place, increment num 
        return num 

    def generate_puzzle_neighbors(self):
        """Method for generating neighboring states from the current puzzle"""
        # saving the location of the empty tile in variables
        empty_tile_row = self.empty_tile_loc["row"] 
        empty_tile_column = self.empty_tile_loc["column"]

        # creating a list to store all neighboring puzzles
        neighboring_puzzle_list = []
        # empty tile has at least one space above 
        if empty_tile_row > 0:
            # create a copy of the current puzzle state
            temp_board = copy.deepcopy(self.puzzle)
            # create a copy of the current empty tile location
            temp_empty_tile_loc = copy.copy(self.empty_tile_loc)
            # create a new puzzle
            temp_puzzle_0 = Puzzle(self.puzzle_size, temp_board, temp_empty_tile_loc)
            # shift the empty tile up
            temp_puzzle_0.swap_tiles(empty_tile_row, empty_tile_column, empty_tile_row - 1, empty_tile_column)
            # add neighbor puzzle to the list
            neighboring_puzzle_list.append(temp_puzzle_0)
        # empty tile has at least one space below
        if empty_tile_row < self.puzzle_size - 1:
            # create a copy of the current puzzle state
            temp_board = copy.deepcopy(self.puzzle)
            # create a copy of the current empty tile location
            temp_empty_tile_loc = copy.copy(self.empty_tile_loc)
            # create a new puzzle
            temp_puzzle_1 = Puzzle(self.puzzle_size, temp_board, temp_empty_tile_loc)
            # shift the empty tile down
            temp_puzzle_1.swap_tiles(empty_tile_row, empty_tile_column, empty_tile_row + 1, empty_tile_column)
            # add neighbor puzzle to the list
            neighboring_puzzle_list.append(temp_puzzle_1)
        # empty tile has at least one space on the left
        if empty_tile_column > 0:
            # create a copy of the current puzzle state
            temp_board = copy.deepcopy(self.puzzle)
            # create a copy of the current empty tile location
            temp_empty_tile_loc = copy.copy(self.empty_tile_loc)
            # create a new puzzle
            temp_puzzle_2 = Puzzle(self.puzzle_size, temp_board, temp_empty_tile_loc)
            # shift the empty tile left
            temp_puzzle_2.swap_tiles(empty_tile_row, empty_tile_column, empty_tile_row, empty_tile_column - 1)
            # add neighbor puzzle to the list
            neighboring_puzzle_list.append(temp_puzzle_2)
        # empty tile has at least one space on the right
        if empty_tile_column < self.puzzle_size - 1:
            # create a copy of the current puzzle state
            temp_board = copy.deepcopy(self.puzzle)
            # create a copy of the current empty tile location
            temp_empty_tile_loc = copy.copy(self.empty_tile_loc)
            # create a new puzzle
            temp_puzzle_3 = Puzzle(self.puzzle_size, temp_board, temp_empty_tile_loc)
            # shift the empty tile right
            temp_puzzle_3.swap_tiles(empty_tile_row, empty_tile_column, empty_tile_row, empty_tile_column + 1)
            # add neight puzzle to the list
            neighboring_puzzle_list.append(temp_puzzle_3)
        # return the neighbor puzzle list
        return neighboring_puzzle_list
