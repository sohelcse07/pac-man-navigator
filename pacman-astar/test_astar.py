"""Tests for the A* implementation and the autonomous Pac-Man.

Run with:  python test_astar.py
(The tests use only the standard library `unittest`, so pytest is optional.)
"""

import unittest
from pathlib import Path

import config
from astar import astar, manhattan_distance
from directions import Direction
from ghost import GhostManager
from grid import Grid
from pacman import Game
import demo


class TestBasicAStar(unittest.TestCase):
    """Test 1 - basic 3x3 path finding."""

    def test_3x3_start_to_goal(self):
        # S . .
        # # # .
        # . . G
        grid = Grid([
            "P..",
            "##.",
            "..." ,
        ])
        start, goal = (0, 0), (2, 2)
        path = astar(start, goal, grid)
        print("Test 1 path:", path)
        self.assertTrue(path, "A* should find a path in the 3x3 grid")
        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], goal)
        # every step must be a single grid move
        for a, b in zip(path, path[1:]):
            self.assertIsNotNone(Direction.from_step(a, b))

    def test_manhattan(self):
        self.assertEqual(manhattan_distance((0, 0), (2, 3)), 5)


class TestWallAvoidance(unittest.TestCase):
    """Test 2 - A* never walks through walls."""

    def test_path_avoids_walls(self):
        grid = Grid([
            "P..",
            "##.",
            "...",
        ])
        path = astar((0, 0), (2, 2), grid)
        for cell in path:
            self.assertFalse(grid.is_wall(cell), "path went through a wall")


class TestUnreachableGoal(unittest.TestCase):
    """Test 3 - a fully blocked goal returns an empty path."""

    def test_no_path(self):
        grid = Grid([
            "P.#",
            "..#",
            "###",
        ])
        # (2, 0) and (2, 1) are walls; build an isolated goal instead.
        grid2 = Grid([
            "P..#..",
            "...#..",
            "...#..",
            "...#..",
        ])
        self.assertEqual(astar((0, 0), (4, 0), grid2), [])
        self.assertEqual(astar((0, 0), (2, 0), grid), [(0, 0), (1, 0), (2, 0)]
                         if not grid.is_wall((2, 0)) else [])


class TestGhostAvoidance(unittest.TestCase):
    """Test 4 - the path never crosses a ghost."""

    def test_path_does_not_cross_ghost(self):
        grid = Grid([
            "P....",
            "#.#.#",
            ".....",
        ])
        ghost_cell = (2, 0)
        path = astar((0, 0), (4, 0), grid, blocked={ghost_cell})
        self.assertTrue(path)
        self.assertNotIn(ghost_cell, path)

    def test_danger_cells_are_expensive_but_not_removed(self):
        grid = Grid(config.MAZE_LAYOUT)
        ghosts = GhostManager(grid.ghost_starts, grid)
        ghost_position = ghosts.positions()[0]
        self.assertGreater(ghosts.danger_cost(ghost_position), 0)
        far_cell = (1, 1)
        self.assertEqual(ghosts.danger_cost(far_cell), 0)

    def test_pacman_never_steps_on_a_ghost(self):
        game = Game(seed=3)
        for _ in range(400):
            if game.finished:
                break
            ghosts_before = set(game.ghosts.positions())
            game.step()
            # Pac-Man may be caught by a ghost that moves onto him, but he
            # must never voluntarily step onto a ghost's current cell.
            self.assertNotIn(game.pacman.position, ghosts_before)


class TestFoodCollection(unittest.TestCase):
    """Test 5 - the full demo collects every pellet."""

    def test_demo_collects_all_food(self):
        game = demo.run_headless(verbose=False, seed=11)
        self.assertTrue(game.won, "Pac-Man did not collect all the food")
        self.assertEqual(game.remaining_food(), 0)


class TestNoKeyboardInput(unittest.TestCase):
    """Test 6 - the game runs with no user input whatsoever."""

    def test_no_input_api_used(self):
        source = open("pacman.py").read() + open("demo.py").read()
        for forbidden in ("input(", "K_UP", "K_LEFT", "K_w", "get_pressed"):
            self.assertNotIn(forbidden, source)

        game = Game(seed=5)
        for _ in range(50):
            game.step()   # no input passed in at any point
        self.assertLess(game.remaining_food(), game.grid.width * game.grid.height)


if __name__ == "__main__":
    unittest.main(verbosity=2)
