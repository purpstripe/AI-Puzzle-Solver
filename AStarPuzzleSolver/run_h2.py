import solution
import time

"""File for running the A* solution with the second heuristic
     - the Manhattan distance for all of the tiles"""

# getting the generated puzzles from the config file
puz_list = solution.get_puzzles_from_config("config_file.csv")

print("heuristic 2")
num_nodes_used = 0
# start time for the A* implementation
start = time.perf_counter()
# iterate through all of the puzzles loaded from config file
for i in range(len(puz_list)):
    print()
    # printing the number of the puzzle
    print("new puz " + str(i+1))
    # run A* on the current puzzle with heuristic 2
    num_nodes_used += solution.a_star(puz_list[i], solution.heuristic_2)[1]

# end time for the A* implementation
end = time.perf_counter()
print()
# print the total time taken
print("total time for all puzzles with heuristic 2: " + str(end - start))
print("the average time to solve each puzzle: " + str( (end - start) / len(puz_list) ))
print("total number of nodes put into the frontier for all puzzles solved: " + str(num_nodes_used))
print("the average number of nodes put into the frontier for each puzzle: " + str(num_nodes_used/len(puz_list)))
