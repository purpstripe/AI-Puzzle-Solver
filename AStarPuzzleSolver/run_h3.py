import solution
import time

"""File for running the A* solution with the third heuristic
    - the number of swaps from the Maxsort algorithm"""

# getting the generated puzzles from the config file
puz_list = solution.get_puzzles_from_config("config_file.csv")

print("heuristic 3")
num_nodes_used = 0
# start time for the A* implementation
start = time.perf_counter()
# iterate through all of the puzzles loaded from the config file
for i in range(len(puz_list)):
    print()
    # printing the number of the puzzle
    print("new puz " + str(i+1))
    # run A* on the curernt puzzle with heuristic 3
    num_nodes_used += solution.a_star(puz_list[i], solution.heuristic_3)[1]
    
# end time for the A* implementation
end = time.perf_counter()
print()
# printing the total time taken
print("total time for all puzzles with heuristic 3: " + str(end - start))
print("the average time to solve each puzzle: " + str( (end - start) / len(puz_list) ))
print("total number of nodes put into the frontier of all puzzles solved: " + str(num_nodes_used))
print("the average number of nodes put into the frontier for each puzzle: " + str(num_nodes_used/len(puz_list)))