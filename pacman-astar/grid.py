"""Grid representation: walls, food, valid positions and neighbours.

The grid knows nothing about pygame or about A*; it is plain data plus a
few small helper methods. That keeps the game logic easy to unit-test.
"""

from directions import Direction
import config


class Grid:
    """A rectangular maze made of walls, corridors and food pellets."""

    def __init__(self, layout=None):
        layout = layout or config.MAZE_LAYOUT
        self.rows = [list(row) for row in layout]
        self.height = len(self.rows)
        self.width = len(self.rows[0])
        if any(len(row) != self.width for row in self.rows):
            raise ValueError("All maze rows must have the same length")

        self.walls = set()
        self.food = set()
        self.pacman_start = None
        self.ghost_starts = []

        self._parse_layout()

    # -- parsing ---------------------------------------------------------
    def _parse_layout(self):
        """Read the character layout into sets of positions."""
        for y, row in enumerate(self.rows):
            for x, char in enumerate(row):
                position = (x, y)
                if char == config.WALL:
                    self.walls.add(position)
                elif char == config.FOOD:
                    self.food.add(position)
                elif char == config.PACMAN_START:
                    self.pacman_start = position
                elif char == config.GHOST_START:
                    self.ghost_starts.append(position)
                    # Ghost cells still contain a pellet to collect.
                    self.food.add(position)

        if self.pacman_start is None:
            raise ValueError("The maze has no Pac-Man start position ('P')")

    # -- queries ---------------------------------------------------------
    def in_bounds(self, position):
        """True when the position lies inside the maze rectangle."""
        x, y = position
        return 0 <= x < self.width and 0 <= y < self.height

    def is_wall(self, position):
        """True when the position is a wall cell."""
        return position in self.walls

    def is_valid_position(self, position):
        """True when Pac-Man/ghosts are allowed to stand on this cell."""
        return self.in_bounds(position) and not self.is_wall(position)

    def get_neighbors(self, position):
        """Return the walkable neighbour cells (up/down/left/right)."""
        neighbors = []
        for direction in Direction:
            candidate = direction.apply(position)
            if self.is_valid_position(candidate):
                neighbors.append(candidate)
        return neighbors

    def has_food(self, position):
        """True when a pellet is still present on this cell."""
        return position in self.food

    def eat_food(self, position):
        """Remove the pellet at `position`; return True when one was eaten."""
        if position in self.food:
            self.food.remove(position)
            return True
        return False

    def remaining_food(self):
        """Number of pellets left on the map."""
        return len(self.food)

    def food_positions(self):
        """A list of all remaining pellet positions."""
        return sorted(self.food)


def parse_grid(text_rows):
    """Build a Grid from a list of strings (handy in tests)."""
    return Grid(text_rows)
