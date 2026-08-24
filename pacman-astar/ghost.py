"""Ghost logic and the safety mechanism used by Pac-Man.

A `Ghost` wanders through the maze with simple rules (keep going, pick a new
random direction at junctions or when blocked). `GhostManager` groups the
ghosts and answers the two questions A* cares about:

    * which cells are strictly blocked (the ghosts themselves)?
    * which cells are merely dangerous (close to a ghost)?

Dangerous cells are NOT removed from the map. They only receive an extra
cost, so Pac-Man walks around them when possible but can still squeeze
through when there is no alternative. That keeps every map solvable.
"""

import random

import config
from astar import manhattan_distance
from directions import Direction


class Ghost:
    """A single ghost moving semi-randomly through the maze."""

    def __init__(self, position, grid, rng=None):
        self.position = position
        self.grid = grid
        self.rng = rng or random.Random()
        self.direction = self.rng.choice(list(Direction))

    def move(self):
        """Take one step: keep the current direction when possible."""
        options = [
            direction
            for direction in Direction
            if self.grid.is_valid_position(direction.apply(self.position))
        ]
        if not options:
            return

        # Prefer to keep going straight, otherwise pick a random legal turn.
        if self.direction in options and self.rng.random() < 0.7:
            chosen = self.direction
        else:
            chosen = self.rng.choice(options)

        self.direction = chosen
        self.position = chosen.apply(self.position)


class GhostManager:
    """Holds every ghost and exposes the danger information."""

    def __init__(self, positions, grid, rng=None):
        rng = rng or random.Random()
        self.grid = grid
        self.ghosts = [Ghost(position, grid, rng) for position in positions]

    # -- detection -------------------------------------------------------
    def positions(self):
        """Current ghost positions."""
        return [ghost.position for ghost in self.ghosts]

    def blocked_cells(self):
        """Cells Pac-Man must never enter: the ghosts and their next cell."""
        blocked = set()
        for ghost in self.ghosts:
            blocked.add(ghost.position)
            # The cell straight ahead of a ghost is a likely head-on collision.
            ahead = ghost.direction.apply(ghost.position)
            if self.grid.is_valid_position(ahead):
                blocked.add(ahead)
        return blocked

    def distance_to_nearest(self, position):
        """Manhattan distance from `position` to the closest ghost."""
        if not self.ghosts:
            return float("inf")
        return min(manhattan_distance(position, g.position) for g in self.ghosts)

    def is_dangerous(self, position):
        """True when a ghost is within GHOST_DANGER_RADIUS cells."""
        return self.distance_to_nearest(position) <= config.GHOST_DANGER_RADIUS

    def danger_cost(self, position):
        """Extra A* cost for a cell: the closer the ghost, the higher."""
        distance = self.distance_to_nearest(position)
        if distance > config.GHOST_DANGER_RADIUS:
            return 0
        # distance 0 -> highest cost, distance == radius -> smallest cost.
        steps_inside = config.GHOST_DANGER_RADIUS - distance + 1
        return config.DANGER_EXTRA_COST * steps_inside

    def collides_with(self, position):
        """True when a ghost currently stands on `position`."""
        return position in set(self.positions())

    # -- simulation ------------------------------------------------------
    def move_all(self):
        """Advance every ghost by one step."""
        for ghost in self.ghosts:
            ghost.move()
