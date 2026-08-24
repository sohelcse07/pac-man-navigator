"""A* pathfinding, implemented from scratch.

The module is completely independent from pygame and from the Pac-Man game
objects: it only needs

* a `start` and a `goal` position, both (x, y) tuples,
* a `grid` object offering `get_neighbors(position)` and `is_valid_position(...)`,
* optionally a set of blocked cells and a cost function for dangerous cells.

Vocabulary (standard A*):
    g-cost : real cost of the cheapest path found so far from start to a node
    h-cost : heuristic estimate from a node to the goal (Manhattan distance)
    f-cost : f(n) = g(n) + h(n) -- the value the open set is sorted by
"""

import heapq


def manhattan_distance(a, b):
    """Manhattan distance heuristic: h(n) = |x1 - x2| + |y1 - y2|.

    It is the right heuristic here because Pac-Man moves on a grid and can
    only step up, down, left or right (no diagonals).
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruct_path(came_from, current):
    """Walk the `came_from` links backwards to build the final path."""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def astar(start, goal, grid, blocked=None, extra_cost=None):
    """Return the cheapest path from `start` to `goal` as a list of cells.

    Arguments:
        start      -- (x, y) starting cell
        goal       -- (x, y) target cell
        grid       -- object with get_neighbors() / is_valid_position()
        blocked    -- optional set of cells that must never be entered
                      (for example the exact ghost positions)
        extra_cost -- optional callable cell -> additional cost, used to make
                      cells near ghosts expensive but still usable as a
                      last resort

    The returned path includes both start and goal, e.g.
        [start, node, node, goal]
    An empty list is returned when no path exists.
    """
    blocked = blocked or set()

    if not grid.is_valid_position(start) or not grid.is_valid_position(goal):
        return []
    if goal in blocked:
        return []
    if start == goal:
        return [start]

    # Open set: a priority queue ordered by f-cost.
    # Each entry is (f_cost, g_cost, position).
    open_heap = [(manhattan_distance(start, goal), 0, start)]
    open_set = {start}

    # Closed set: nodes we already expanded and never need to revisit.
    closed_set = set()

    came_from = {}
    g_costs = {start: 0}

    while open_heap:
        _, current_g, current = heapq.heappop(open_heap)
        open_set.discard(current)

        if current in closed_set:
            continue
        closed_set.add(current)

        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor in grid.get_neighbors(current):
            if neighbor in closed_set or neighbor in blocked:
                continue

            step_cost = 1
            if extra_cost is not None:
                step_cost += extra_cost(neighbor)

            tentative_g = current_g + step_cost
            if tentative_g < g_costs.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_costs[neighbor] = tentative_g
                f_cost = tentative_g + manhattan_distance(neighbor, goal)
                heapq.heappush(open_heap, (f_cost, tentative_g, neighbor))
                open_set.add(neighbor)

    # The open set ran empty: the goal cannot be reached.
    return []


def path_cost(path, extra_cost=None):
    """Total cost of a path (number of steps plus any danger penalties)."""
    if not path:
        return float("inf")
    cost = len(path) - 1
    if extra_cost is not None:
        for cell in path[1:]:
            cost += extra_cost(cell)
    return cost
