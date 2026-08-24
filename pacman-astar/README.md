# Pac-Man A* Pathfinding — Phase 4

An autonomous Pac-Man: the player is controlled entirely by an A* search
implemented from scratch. Pac-Man detects its position, the remaining food,
the walls and the ghosts, picks a safe target, computes the shortest safe
path and follows it — replanning whenever the ghosts move. **No keyboard
input is required or used.**

---

## 1. Project Overview

The project renders a classic Pac-Man maze with pygame and lets an
algorithm play it. Each frame Pac-Man:

1. detects its current cell,
2. lists the remaining food,
3. asks the grid which cells are walls,
4. asks the ghost manager which cells are blocked or dangerous,
5. runs A* to every reachable pellet and keeps the cheapest safe one,
6. steps one cell along that path,
7. recalculates whenever the path becomes unsafe or the pellet is eaten,

until every pellet is collected.

## 2. A* Explanation

A* is a best-first graph search that always expands the node with the
smallest estimated total cost:

```
f(n) = g(n) + h(n)
```

* **g-cost** — the real cost of the cheapest known path from the start to
  node `n` (here: number of steps + danger penalties).
* **h-cost** — an optimistic estimate of the remaining cost from `n` to the
  goal.
* **f-cost** — their sum; the open set (a priority queue) is ordered by it.
* **Open set** — nodes discovered but not expanded yet.
* **Closed set** — nodes already expanded; never revisited.

The heuristic is the **Manhattan distance**:

```
h(n) = abs(x1 - x2) + abs(y1 - y2)
```

which is exact for a 4-direction grid and therefore never overestimates —
that makes A* both correct and fast. A* fits Pac-Man perfectly: the maze is
a small grid graph, movement is unit-cost, and the heuristic guides the
search straight towards the target instead of flooding the whole maze like
BFS/Dijkstra would.

## 3. Architecture

| Module | Responsibility |
| --- | --- |
| `config.py` | Maze layout, colours, speed, danger radius and costs. |
| `directions.py` | `Direction` Enum (`UP/DOWN/LEFT/RIGHT`) with `(dx, dy)` deltas, `apply()` and `from_step()`. |
| `grid.py` | Grid parsing, `is_wall()`, `is_valid_position()`, `get_neighbors()`, food tracking. |
| `astar.py` | Pure A* (`astar`, `manhattan_distance`, `path_cost`). No UI, no game objects. |
| `ghost.py` | `Ghost` movement + `GhostManager` (positions, blocked cells, `is_dangerous`, `danger_cost`). |
| `pacman.py` | `PacMan` (target selection, path following, replanning) and `Game` (one `step()` per frame). |
| `main.py` | pygame rendering: walls, food, ghosts, Pac-Man, highlighted A* path, HUD. |
| `demo.py` | Entry point: graphical demo with automatic headless fallback. |
| `test_astar.py` | Tests 1–6 from the assignment. |

## 4. How Ghost Avoidance Works

Two levels of safety, so the map always stays solvable:

* **Hard blocked** — a ghost's current cell and the cell directly in front
  of it are removed from the search. A* can never plan through them.
* **Soft danger** — cells within `GHOST_DANGER_RADIUS` (2) get an extra
  A* cost (`DANGER_EXTRA_COST` scaled by closeness). Pac-Man detours around
  them when a detour exists, but can still pass through if that is the only
  way — dangerous cells are never deleted from the map.

Every frame Pac-Man checks the next few cells of its path; if any became
blocked or dangerous the path is thrown away and A* runs again. If ghosts
temporarily fence Pac-Man in, a fallback search runs without the danger
penalty (still never entering a ghost cell); if even that fails, Pac-Man
waits safely and retries next frame.

## 5. How Food Selection Works

Pac-Man does not pick a random pellet:

1. list every remaining pellet,
2. run A* to each one with ghost cells blocked and danger costs applied,
3. skip pellets with no path (unreachable),
4. keep the pellet with the **lowest total path cost** (steps + danger),
5. follow that path, eat the pellet, and repeat.

Because danger is part of the cost, a slightly farther but safer pellet
wins over a close pellet sitting next to a ghost.

## 6. Installation

```bash
cd pacman-astar
python -m pip install -r requirements.txt
```

Requires Python 3.8+ and pygame 2.x.

## 7. Running the Demo

```bash
python demo.py            # graphical, fully automatic
python demo.py --headless # console-only simulation (no display needed)
python main.py            # graphical window directly
```

## 8. Running Tests

```bash
python test_astar.py
```

(`python -m pytest test_astar.py` also works if pytest is installed.)

## 9. Expected Result

Pac-Man starts moving immediately, highlights its A* path, avoids ghosts and
keeps eating until the console prints:

```
All food collected!
Demo completed successfully in 239 steps. Score: 1430
```

No arrow keys, no WASD, no user interaction at any point.

## 10. Limitations

* The maze, ghost art and sprites are simplified into coloured shapes; the
  original skeleton's bitmap assets are not used so the project runs from a
  clean checkout with no image files.
* Ghosts wander semi-randomly (keep direction, random turn at junctions)
  instead of using the original chase/scatter AI, so danger is stochastic.
* Being caught is not fatal: Pac-Man loses a few points and replans. This
  keeps the "collect all food" objective always achievable, which is what
  Phase 4 grades.
* A* replans from scratch each time; this is fast for this maze size but is
  not optimised for very large maps.
* Power pellets, fruit, tunnels and multiple lives are out of scope.
