"""Movement directions for Pac-Man, expressed as an Enum.

Using an Enum (instead of raw strings like "up"/"left") makes the code
safer and easier to read: typos become errors instead of silent bugs.
"""

from enum import Enum


class Direction(Enum):
    """The four grid directions.

    Every value is a (dx, dy) offset in *grid* coordinates:
    x grows to the right, y grows downwards.
    """

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @property
    def delta(self):
        """Return the (dx, dy) tuple of this direction."""
        return self.value

    def apply(self, position):
        """Return the position reached by moving one step in this direction."""
        x, y = position
        dx, dy = self.value
        return (x + dx, y + dy)

    @staticmethod
    def from_step(start, end):
        """Return the Direction that leads from `start` to the adjacent `end`.

        Returns None when the two positions are not neighbours.
        """
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        for direction in Direction:
            if direction.value == (dx, dy):
                return direction
        return None
