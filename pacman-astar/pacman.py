"""Pac-Man game logic driven entirely by A* (no keyboard input).

`PacMan` is the autonomous agent: it detects its position, the remaining
food, the walls and the ghosts, chooses a safe target and follows the A*
path. `Game` glues the grid, the ghosts and Pac-Man together and exposes a
single `step()` method that the demo / UI calls once per frame.
"""

import random

import config
from astar import astar, path_cost
from directions import Direction
from ghost import GhostManager
from grid import Grid


class PacMan:
    """The automated player."""

    def __init__(self, position, grid, ghosts):
        self.position = position
        self.grid = grid
        self.ghosts = ghosts
        self.path = []          # remaining cells of the current A* path
        self.target = None      # food cell we are heading to
        self.direction = Direction.LEFT
        self.score = 0

    # -- perception ------------------------------------------------------
    def danger_cost(self, cell):
        """Extra cost used by A* to keep away from ghosts."""
        return self.ghosts.danger_cost(cell)

    def _blocked_cells(self):
        return self.ghosts.blocked_cells()

    # -- planning --------------------------------------------------------
    def choose_target_and_path(self):
        """Pick the cheapest *safe* reachable food and plan the path to it.

        Strategy:
          1. Look at every remaining pellet.
          2. Run A* (ghost cells blocked, nearby cells expensive).
          3. Ignore unreachable pellets.
          4. Keep the one with the lowest total cost.
          5. If nothing is reachable while avoiding ghosts, retry once
             without the danger penalty so Pac-Man is never stuck.
        """
        foods = self.grid.food_positions()
        if not foods:
            self.target, self.path = None, []
            return []

        blocked = self._blocked_cells()
        blocked.discard(self.position)

        best_path = self._best_path_to_food(foods, blocked, self.danger_cost)
        if not best_path:
            # Fallback: ghosts fence us in -- try again ignoring the danger
            # penalty, but still never stepping onto a ghost itself.
            hard_blocked = set(self.ghosts.positions())
            hard_blocked.discard(self.position)
            best_path = self._best_path_to_food(foods, hard_blocked, None)

        if best_path:
            self.target = best_path[-1]
            self.path = best_path[1:]      # drop the current cell
        else:
            self.target, self.path = None, []
        return best_path

    def _best_path_to_food(self, foods, blocked, extra_cost):
        """Return the lowest-cost A* path to any of the given food cells."""
        best_path = []
        best_cost = float("inf")
        for food in foods:
            path = astar(self.position, food, self.grid,
                         blocked=blocked, extra_cost=extra_cost)
            if not path:
                continue
            cost = path_cost(path, extra_cost)
            if cost < best_cost:
                best_cost, best_path = cost, path
        return best_path

    def path_is_unsafe(self):
        """True when the next couple of steps became dangerous or blocked."""
        if not self.path:
            return True
        blocked = self._blocked_cells()
        for cell in self.path[:3]:
            if cell in blocked or self.ghosts.is_dangerous(cell):
                return True
        return False

    # -- acting ----------------------------------------------------------
    def step(self):
        """Move one cell along the current path, replanning when needed.

        Returns a small dict describing what happened (used by the demo to
        print progress information).
        """
        info = {"replanned": False, "ate": False, "moved": False,
                "stuck": False, "target": self.target}

        if self.path_is_unsafe() or self.target is None or not self.path:
            self.choose_target_and_path()
            info["replanned"] = True
            info["target"] = self.target

        if not self.path:
            info["stuck"] = True
            return info

        next_cell = self.path[0]
        if not self.grid.is_valid_position(next_cell):
            self.path = []
            info["stuck"] = True
            return info

        # Never walk straight into a ghost.
        if self.ghosts.collides_with(next_cell):
            self.path = []
            info["stuck"] = True
            return info

        direction = Direction.from_step(self.position, next_cell)
        if direction is not None:
            self.direction = direction
        self.position = self.path.pop(0)
        info["moved"] = True

        if self.grid.eat_food(self.position):
            self.score += 10
            info["ate"] = True
            self.target, self.path = None, []

        return info


class Game:
    """The whole simulation: maze + ghosts + autonomous Pac-Man."""

    def __init__(self, layout=None, seed=None):
        self.grid = Grid(layout)
        rng = random.Random(seed)
        self.ghosts = GhostManager(self.grid.ghost_starts, self.grid, rng)
        self.pacman = PacMan(self.grid.pacman_start, self.grid, self.ghosts)
        self.frame = 0
        self.finished = False
        self.won = False
        self.caught = False

    # -- state -----------------------------------------------------------
    def remaining_food(self):
        return self.grid.remaining_food()

    # -- simulation ------------------------------------------------------
    def step(self):
        """Advance the game by one frame and return Pac-Man's step info."""
        if self.finished:
            return {"finished": True}

        self.frame += 1
        info = self.pacman.step()

        if self.frame % config.GHOST_MOVE_EVERY == 0:
            self.ghosts.move_all()

        if self.ghosts.collides_with(self.pacman.position):
            # Being caught is not fatal in this demo: Pac-Man simply loses a
            # little score and immediately replans a safer route.
            self.caught = True
            self.pacman.score = max(0, self.pacman.score - 5)
            self.pacman.path = []
            self.pacman.target = None

        if self.remaining_food() == 0:
            self.finished = True
            self.won = True

        info["finished"] = self.finished
        return info
