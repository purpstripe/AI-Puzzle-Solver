import unittest
import puzzle

class TestPuzzle(unittest.TestCase):

    def test_get_one_dim_puzzle(self):
        lst = [0,1,2,3]
        puz = puzzle.Puzzle(2, [[0,1],[2,3]], {"row": 0, "column": 0})
        self.assertEqual(puz.get_one_dim_puzzle(), lst)

        lst = [2,1,0,3]
        puz = puzzle.Puzzle(2, [[2,1],[0,3]], {"row": 1, "column": 0})
        self.assertEqual(puz.get_one_dim_puzzle(), lst)

        lst = [2,1,3,0]
        puz = puzzle.Puzzle(2, [[2,1],[3,0]], {"row": 1, "column": 1})
        self.assertEqual(puz.get_one_dim_puzzle(), lst)

        lst = [0,1,2,3,4,5,6,7,8]
        puz = puzzle.Puzzle(3, [[0,1,2],[3,4,5],[6,7,8]], {"row": 0, "column": 0})
        self.assertEqual(puz.get_one_dim_puzzle(), lst)

        lst = [1,4,2,3,0,5,6,7,8]
        puz = puzzle.Puzzle(3, [[1,4,2], [3,0,5], [6,7,8]], {"row": 1, "column": 1})
        self.assertEqual(puz.get_one_dim_puzzle(), lst)

        lst = [1,4,2,3,5,0,6,7,8]
        puz = puzzle.Puzzle(3, [[1,4,2], [3,5,0], [6,7,8]], {"row": 1, "column": 2})
        self.assertEqual(puz.get_one_dim_puzzle(), lst)

        lst = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        puz = puzzle.Puzzle(4, [[0,1,2,3], [4,5,6,7], [8,9,10,11], [12,13,14,15]], {"row": 0, "column": 0})
        self.assertEqual(puz.get_one_dim_puzzle(), lst)

        lst = [4,1,2,3,8,5,6,7,9,0,10,11,12,13,14,15]
        puz = puzzle.Puzzle(4, [[4,1,2,3], [8,5,6,7], [9,0,10,11], [12,13,14,15]], {"row": 2, "column": 1})
        self.assertEqual(puz.get_one_dim_puzzle(), lst)

        lst = [4,1,2,3,8,5,6,7,9,10,14,11,12,13,0,15]
        puz = puzzle.Puzzle(4, [[4,1,2,3], [8,5,6,7], [9,10,14,11], [12,13,0,15]], {"row": 3, "column": 2})
        self.assertEqual(puz.get_one_dim_puzzle(), lst)

    def test_find_empty_tile(self):
        empty_loc = {"row": 0, "column": 0}
        puz = puzzle.Puzzle(2, [[0,1], [2,3]], empty_loc)
        self.assertEqual(puz.find_empty_tile(), empty_loc)

        empty_loc = {"row": 0, "column": 1}
        puz = puzzle.Puzzle(2, [[1,0], [2,3]], empty_loc)
        self.assertEqual(puz.find_empty_tile(), empty_loc)

        empty_loc = {"row": 1, "column": 1}
        puz = puzzle.Puzzle(2, [[1,3], [2,0]], empty_loc)
        self.assertEqual(puz.find_empty_tile(), empty_loc)

        empty_loc = {"row": 0, "column": 0}
        puz = puzzle.Puzzle(3, [[0,1,2], [3,4,5], [6,7,8]], empty_loc)
        self.assertEqual(puz.find_empty_tile(), empty_loc)
        
        empty_loc = {"row": 1, "column": 1}
        puz = puzzle.Puzzle(3, [[1,4,2], [3,0,5], [6,7,8]], empty_loc)
        self.assertEqual(puz.find_empty_tile(), empty_loc)

        empty_loc = {"row": 2, "column": 0}
        puz = puzzle.Puzzle(3, [[1,4,2], [3,7,5], [0,6,8]], empty_loc)
        self.assertEqual(puz.find_empty_tile(), empty_loc)

        empty_loc = {"row": 0, "column": 0}
        puz = puzzle.Puzzle(4, [[0,1,2,3], [4,5,6,7], [8,9,10,11], [12,13,14,15]], empty_loc)
        self.assertEqual(puz.find_empty_tile(), empty_loc)

        empty_loc = {"row": 1, "column": 2}
        puz = puzzle.Puzzle(4, [[1,2,6,3], [4,5,0,7], [8,9,10,11], [12,13,14,15]], empty_loc)
        self.assertEqual(puz.find_empty_tile(), empty_loc)

        empty_loc = {"row": 2, "column": 3}
        puz = puzzle.Puzzle(4, [[1,2,6,3], [4,5,10,7], [8,9,11,0], [12,13,14,15]], empty_loc)
        self.assertEqual(puz.find_empty_tile(), empty_loc)

    def test_set_puzzle(self):
        puz = puzzle.Puzzle(2, [[0,1],[2,3]], {"row": 0, "column": 0})
        puz.set_puzzle([[1,0],[2,3]])
        self.assertEqual(puz.puzzle, [[1,0],[2,3]]) 
        self.assertEqual(puz.empty_tile_loc, {"row": 0, "column": 1})
        puz.set_puzzle([[1,3],[2,0]])
        self.assertEqual(puz.puzzle, [[1,3],[2,0]]) 
        self.assertEqual(puz.empty_tile_loc, {"row": 1, "column": 1})
        puz.set_puzzle([[1,3],[0,2]])
        self.assertEqual(puz.puzzle, [[1,3],[0,2]]) 
        self.assertEqual(puz.empty_tile_loc, {"row": 1, "column": 0})

    def test_swap_tiles(self):
        puz = puzzle.Puzzle(2, [[0,1],[2,3]], {"row": 0, "column": 0})
        puz.swap_tiles(0,0,1,0)
        self.assertEqual(puz.puzzle, [[2,1],[0,3]])
        self.assertEqual(puz.empty_tile_loc, {"row": 1, "column": 0})
        puz.swap_tiles(0,1,1,1)
        self.assertEqual(puz.puzzle, [[2,3],[0,1]])
        self.assertEqual(puz.empty_tile_loc, {"row": 1, "column": 0})

        puz = puzzle.Puzzle(3, [[0,1,2],[3,4,5],[6,7,8]], {"row": 0, "column": 0})
        puz.swap_tiles(0,0,0,1)
        self.assertEqual(puz.puzzle, [[1,0,2],[3,4,5],[6,7,8]])
        self.assertEqual(puz.empty_tile_loc, {"row": 0, "column": 1})
        puz.swap_tiles(0,1,1,1)
        self.assertEqual(puz.puzzle, [[1,4,2],[3,0,5],[6,7,8]])
        self.assertEqual(puz.empty_tile_loc, {"row": 1, "column": 1})
        puz.swap_tiles(1,1,2,1)
        puz.swap_tiles(2,1,2,2)
        self.assertEqual(puz.puzzle, [[1,4,2],[3,7,5],[6,8,0]])
        self.assertEqual(puz.empty_tile_loc, {"row": 2, "column": 2})
        puz.swap_tiles(1,1,1,0)
        self.assertEqual(puz.puzzle, [[1,4,2],[7,3,5],[6,8,0]])
        self.assertEqual(puz.empty_tile_loc, {"row": 2, "column": 2})

        puz = puzzle.Puzzle(4, [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]], {"row": 0, "column": 0})
        puz.swap_tiles(0,0,1,0)
        self.assertEqual(puz.puzzle, [[4,1,2,3],[0,5,6,7],[8,9,10,11],[12,13,14,15]])
        self.assertEqual(puz.empty_tile_loc, {"row": 1, "column": 0})
        puz.swap_tiles(1,0,1,1)
        self.assertEqual(puz.puzzle, [[4,1,2,3],[5,0,6,7],[8,9,10,11],[12,13,14,15]])
        self.assertEqual(puz.empty_tile_loc, {"row": 1, "column": 1})
        puz.swap_tiles(1,1,1,2)
        self.assertEqual(puz.puzzle, [[4,1,2,3],[5,6,0,7],[8,9,10,11],[12,13,14,15]])
        self.assertEqual(puz.empty_tile_loc, {"row": 1, "column": 2})
        puz.swap_tiles(1,2,2,2)
        self.assertEqual(puz.puzzle, [[4,1,2,3],[5,6,10,7],[8,9,0,11],[12,13,14,15]])
        self.assertEqual(puz.empty_tile_loc, {"row": 2, "column": 2})
        puz.swap_tiles(1,1,1,2)
        self.assertEqual(puz.puzzle, [[4,1,2,3],[5,10,6,7],[8,9,0,11],[12,13,14,15]])
        self.assertEqual(puz.empty_tile_loc, {"row": 2, "column": 2})
        puz.swap_tiles(3,2,3,3)
        self.assertEqual(puz.puzzle, [[4,1,2,3],[5,10,6,7],[8,9,0,11],[12,13,15,14]])
        self.assertEqual(puz.empty_tile_loc, {"row": 2, "column": 2})
        puz.swap_tiles(3,2,2,2)
        self.assertEqual(puz.puzzle, [[4,1,2,3],[5,10,6,7],[8,9,15,11],[12,13,0,14]])
        self.assertEqual(puz.empty_tile_loc, {"row": 3, "column": 2})

    def test_is_puzzle_equal(self):
        puz0 = puzzle.Puzzle(2, [[0,1],[2,3]], {"row": 0, "column": 0})
        puz1 = puzzle.Puzzle(2, [[0,1],[2,3]], {"row": 0, "column": 0})
        self.assertTrue(puz0.is_puzzle_equal(puz0))
        self.assertTrue(puz1.is_puzzle_equal(puz1))
        self.assertTrue(puz0.is_puzzle_equal(puz1))
        self.assertTrue(puz1.is_puzzle_equal(puz0))
        puz0 = puzzle.Puzzle(2, [[0,1],[2,3]], {"row": 0, "column": 0})
        puz1 = puzzle.Puzzle(2, [[1,0],[2,3]], {"row": 0, "column": 1})
        self.assertFalse(puz0.is_puzzle_equal(puz1))
        self.assertFalse(puz1.is_puzzle_equal(puz0))
        puz0 = puzzle.Puzzle(2, [[0,3],[2,1]], {"row": 0, "column": 0})
        puz1 = puzzle.Puzzle(2, [[0,3],[2,1]], {"row": 0, "column": 0})
        self.assertTrue(puz0.is_puzzle_equal(puz1))
        self.assertTrue(puz1.is_puzzle_equal(puz0))
        puz0 = puzzle.Puzzle(2, [[3,0],[2,1]], {"row": 0, "column": 1})
        puz1 = puzzle.Puzzle(2, [[0,3],[2,1]], {"row": 0, "column": 0})
        self.assertFalse(puz0.is_puzzle_equal(puz1))
        self.assertFalse(puz1.is_puzzle_equal(puz0))

        puz0 = puzzle.Puzzle(3, [[0,1,2], [3,4,5], [6,7,8]], {"row": 0, "column": 0})
        puz1 = puzzle.Puzzle(3, [[0,1,2], [3,4,5], [6,7,8]], {"row": 0, "column": 0})
        self.assertTrue(puz0.is_puzzle_equal(puz0))
        self.assertTrue(puz1.is_puzzle_equal(puz1))
        self.assertTrue(puz0.is_puzzle_equal(puz1))
        self.assertTrue(puz1.is_puzzle_equal(puz0))
        puz0 = puzzle.Puzzle(3, [[1,2,0], [3,4,5], [6,7,8]], {"row": 0, "column": 2})
        puz1 = puzzle.Puzzle(3, [[0,1,2], [3,4,5], [6,7,8]], {"row": 0, "column": 0})
        self.assertFalse(puz0.is_puzzle_equal(puz1))
        self.assertFalse(puz1.is_puzzle_equal(puz0))
        puz0 = puzzle.Puzzle(3, [[1,2,5], [3,4,0], [6,7,8]], {"row": 1, "column": 2})
        puz1 = puzzle.Puzzle(3, [[1,0,2], [3,4,5], [6,7,8]], {"row": 0, "column": 1})
        self.assertFalse(puz0.is_puzzle_equal(puz1))
        self.assertFalse(puz1.is_puzzle_equal(puz0))
        puz0 = puzzle.Puzzle(3, [[3,1,2], [0,4,5], [6,7,8]], {"row": 1, "column": 0})
        puz1 = puzzle.Puzzle(3, [[3,1,2], [0,4,5], [6,7,8]], {"row": 1, "column": 0})
        self.assertTrue(puz0.is_puzzle_equal(puz1))
        self.assertTrue(puz1.is_puzzle_equal(puz0))

        puz0 = puzzle.Puzzle(4, [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]], {"row": 0, "column": 0})
        puz1 = puzzle.Puzzle(4, [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]], {"row": 0, "column": 0})
        self.assertTrue(puz0.is_puzzle_equal(puz0))
        self.assertTrue(puz1.is_puzzle_equal(puz1))
        self.assertTrue(puz0.is_puzzle_equal(puz1))
        self.assertTrue(puz1.is_puzzle_equal(puz0))
        puz0 = puzzle.Puzzle(4, [[0,2,1,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]], {"row": 0, "column": 0})
        puz1 = puzzle.Puzzle(4, [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]], {"row": 0, "column": 0})
        self.assertFalse(puz0.is_puzzle_equal(puz1))
        self.assertFalse(puz1.is_puzzle_equal(puz0))
        puz0 = puzzle.Puzzle(4, [[0,2,1,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]], {"row": 0, "column": 0})
        puz1 = puzzle.Puzzle(4, [[0,2,1,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]], {"row": 0, "column": 0})
        self.assertTrue(puz0.is_puzzle_equal(puz1))
        self.assertTrue(puz1.is_puzzle_equal(puz0))
        puz0 = puzzle.Puzzle(4, [[4,2,1,3],[0,5,6,7],[8,9,10,11],[12,13,14,15]], {"row": 1, "column": 0})
        puz1 = puzzle.Puzzle(4, [[4,2,1,3],[0,5,6,7],[8,9,10,11],[12,13,14,15]], {"row": 1, "column": 0})
        self.assertTrue(puz0.is_puzzle_equal(puz1))
        self.assertTrue(puz1.is_puzzle_equal(puz0))
        puz0 = puzzle.Puzzle(4, [[4,2,1,3],[8,5,6,7],[9,0,10,11],[12,13,14,15]], {"row": 2, "column": 1})
        puz1 = puzzle.Puzzle(4, [[4,2,1,3],[0,5,6,7],[8,9,10,11],[12,13,14,15]], {"row": 1, "column": 0})
        self.assertFalse(puz0.is_puzzle_equal(puz1))
        self.assertFalse(puz1.is_puzzle_equal(puz0))

    def test_is_puzzle_solved(self):
        puz = puzzle.Puzzle(2, [[0,1],[2,3]], {"row": 0, "column": 0})
        self.assertTrue(puz.is_puzzle_solved())
        puz = puzzle.Puzzle(2, [[1,0],[2,3]], {"row": 0, "column": 1})
        self.assertFalse(puz.is_puzzle_solved())
        puz = puzzle.Puzzle(2, [[2,1],[0,3]], {"row": 1, "column": 0})
        self.assertFalse(puz.is_puzzle_solved())
        puz = puzzle.Puzzle(2, [[2,1],[3,0]], {"row": 1, "column": 1})
        self.assertFalse(puz.is_puzzle_solved())

        puz = puzzle.Puzzle(3, [[0,1,2],[3,4,5],[6,7,8]], {"row": 0, "column": 0})
        self.assertTrue(puz.is_puzzle_solved())
        puz = puzzle.Puzzle(3, [[1,0,2],[3,4,5],[6,7,8]], {"row": 0, "column": 1})
        self.assertFalse(puz.is_puzzle_solved())
        puz = puzzle.Puzzle(3, [[1,4,2],[3,0,5],[6,7,8]], {"row": 1, "column": 1})
        self.assertFalse(puz.is_puzzle_solved())
        puz = puzzle.Puzzle(3, [[1,4,2],[3,5,0],[6,7,8]], {"row": 1, "column": 2})
        self.assertFalse(puz.is_puzzle_solved())
        puz = puzzle.Puzzle(3, [[1,4,2],[3,5,8],[6,7,0]], {"row": 2, "column": 2})
        self.assertFalse(puz.is_puzzle_solved())
        puz = puzzle.Puzzle(3, [[1,4,2],[0,3,5],[6,7,8]], {"row": 1, "column": 0})
        self.assertFalse(puz.is_puzzle_solved())
        puz = puzzle.Puzzle(3, [[0,4,2],[1,3,5],[6,7,8]], {"row": 0, "column": 0})
        self.assertFalse(puz.is_puzzle_solved())

        puz = puzzle.Puzzle(4, [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]], {"row": 0, "column": 0})
        self.assertTrue(puz.is_puzzle_solved())

if __name__ == "__main__":
    unittest.main()