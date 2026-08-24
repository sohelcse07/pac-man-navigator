"""Central configuration: the maze layout, colours and timing.

Everything a beginner may want to tweak lives in this single file.
"""

# --- Maze legend ---------------------------------------------------------
# '#' wall
# '.' food pellet
# ' ' empty corridor (no food)
# 'P' Pac-Man start position (the cell also stays empty)
# 'G' ghost start position (the cell also contains food)
WALL = "#"
FOOD = "."
EMPTY = " "
PACMAN_START = "P"
GHOST_START = "G"

# The default maze. Every row must have the same length.
MAZE_LAYOUT = [
    "###################",
    "#........#........#",
    "#.##.###.#.###.##.#",
    "#.................#",
    "#.##.#.#####.#.##.#",
    "#....#...#...#....#",
    "####.###.#.###.####",
    "#.......GGG.......#",
    "####.###.#.###.####",
    "#....#...#...#....#",
    "#.##.#.#####.#.##.#",
    "#.................#",
    "#.##.###.#.###.##.#",
    "#........P........#",
    "###################",
]

# --- Rendering -----------------------------------------------------------
CELL_SIZE = 28          # pixels per grid cell
HUD_HEIGHT = 40         # space at the bottom for the score text
FPS = 10                # game speed: Pac-Man moves one cell per frame

COLOR_BACKGROUND = (0, 0, 0)
COLOR_WALL = (33, 33, 222)
COLOR_FOOD = (255, 214, 153)
COLOR_PACMAN = (255, 235, 59)
COLOR_GHOST = (244, 67, 54)
COLOR_PATH = (0, 200, 120)      # highlighted A* path
COLOR_TARGET = (0, 230, 255)    # currently selected food target
COLOR_TEXT = (240, 240, 240)

# --- Gameplay ------------------------------------------------------------
GHOST_MOVE_EVERY = 2        # ghosts move once every N frames (slower than Pac-Man)
GHOST_DANGER_RADIUS = 2     # cells within this distance of a ghost are "dangerous"
DANGER_EXTRA_COST = 12      # extra A* cost for stepping on a dangerous cell
MAX_DEMO_STEPS = 6000       # safety limit so a demo can never loop forever
