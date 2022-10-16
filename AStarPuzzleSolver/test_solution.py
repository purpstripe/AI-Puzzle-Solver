import unittest
import solution
import puzzle
import generator


print()
print("testing finding the correct location of a given tile") 
for i in range(2, 5):
    for j in range(i**2):
        print("tile " + str(j) + " size " + str(i))
        print("correct loc " + str(solution.get_correct_tile_loc(j, i) ))
        print("\n")

print("testing heuristics on shuffled puzzle")
puz = puzzle.Puzzle(3)
puz.set_solution_puzzle()
puz = generator.shuffle_puzzle(puz)
h1 = solution.heuristic_1(puz)
print("h1: " + str(h1))
h2 = solution.heuristic_2(puz)
print("h2: " + str(h2))
h3 = solution.heuristic_3(puz)
print("h3: " + str(h3))
h4 = solution.heuristic_4(puz)
print("h4: " + str(h4))

print("testing getting min node from frontier")
puz0 = puzzle.Puzzle(3)
puz0.set_solution_puzzle()
puz0 = generator.shuffle_puzzle(puz0)
node0 = solution.Node(puz0,1)
puz1 = puzzle.Puzzle(3)
puz1.set_solution_puzzle()
puz1 = generator.shuffle_puzzle(puz1)
node1 = solution.Node(puz1,2)
puz2 = puzzle.Puzzle(3)
puz2.set_solution_puzzle()
puz2 = generator.shuffle_puzzle(puz2)
node2 = solution.Node(puz2,3)
puz3 = puzzle.Puzzle(3)
puz3.set_solution_puzzle()
puz3 = generator.shuffle_puzzle(puz3)
node3 = solution.Node(puz3,4)
node_list = [node0, node1, node2, node3]
print()
print("testing generating child nodes")
puz = puzzle.Puzzle(3)
puz.set_solution_puzzle()
print("inital puzzle")
print(puz)
print()
node = solution.Node(puz, 0)
lst = solution.expand(node)
for n in lst:
    print("neighbor:")
    print(n)
    print()

puz = puzzle.Puzzle(3)
puz.set_solution_puzzle()
puz = generator.shuffle_puzzle(puz)
print("inital puzzle")
print(puz)
print()
node = solution.Node(puz, 0)
lst = solution.expand(node)
for n in lst:
    print("neighbor:")
    print(n)
    print()