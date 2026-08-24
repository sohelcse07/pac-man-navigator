# Pac-Man Navigator

Build and complete Phase 4: Pac-Man A Pathfinding* as a fully working Python project based on the assignment requirements below.
Assignment
Phase 4: Pac-Man A* Pathfinding
Points: 40
Goal: Implement A* pathfinding for automated Pac-Man so that Pac-Man can collect all food items without keyboard input while avoiding ghosts.
Main Objectives
Implement the A* search algorithm for automated Pac-Man pathfinding.
Refactor and modularize the existing Pac-Man code.
Use Enums for movement directions.
Implement reliable wall detection.
Implement ghost detection and ghost avoidance.
Make Pac-Man automatically find paths to food.
Pac-Man must collect all available food items.
Pac-Man must run completely automatically with NO keyboard input required.
The final project should be clean, understandable, modular, and beginner-friendly.
Reference Code
Use this Pac-Man Python skeleton as the starting point:
https://github.com/hbokmann/Pacman/blob/master/pacman.py
Do NOT blindly copy the entire code. Refactor it where necessary and integrate A* properly.
Important Requirement
The final application must demonstrate that Pac-Man can autonomously:
Detect the current position.
Detect remaining food.
Detect walls/blocked cells.
Detect ghost positions.
Choose a safe food target.
Calculate the shortest/safest path using A*.
Follow the calculated path automatically.
Recalculate the path when the environment changes.
Avoid moving into ghosts whenever possible.
Continue until all food is collected.
There must be no requirement for the user to press arrow keys or WASD.
A* Implementation
Implement A* from scratch.
Use the standard concepts:
Open set
Closed set
g-cost
h-cost
f-cost
Where:
f(n) = g(n) + h(n)
For the heuristic, use Manhattan Distance because Pac-Man moves on a grid:
h(n) = abs(x1 - x2) + abs(y1 - y2)
The algorithm should return the best path from Pac-Man's current position to the selected food position.
Example:
Start → Node → Node → Node → Food

The path should avoid walls and dangerous ghost positions.
Beginner Testing First
Before integrating A* into Pac-Man, create a small independent 3×3 grid test.
Example:
S . .
# # .
. . G

Where:
S = Start
G = Goal
= Wall
The program should calculate and print the A* path.
This test should prove that the A* implementation works independently before Pac-Man integration.
Suggested Project Structure
Create a clean modular structure similar to:
pacman-astar/
│
├── main.py
├── pacman.py
├── astar.py
├── directions.py
├── grid.py
├── ghost.py
├── config.py
├── demo.py
├── test_astar.py
├── README.md
└── requirements.txt

You may modify the structure if the original skeleton requires a different organization, but keep the code modular.
Module Responsibilities
directions.py
Create an Enum such as:
from enum import Enum

class Direction(Enum):
    UP = ...
    DOWN = ...
    LEFT = ...
    RIGHT = ...

Use this Enum instead of repeatedly using raw strings throughout the project.
astar.py
Implement:
astar(start, goal, grid, ...)

Responsibilities:
Calculate paths.
Handle walls.
Handle blocked/dangerous cells.
Use Manhattan heuristic.
Return the path.
Return an empty path or appropriate result if no path exists.
Keep this module independent from the Pac-Man UI as much as possible.
grid.py
Handle:
Grid representation.
Wall detection.
Valid positions.
Neighbor cells.
Collision checking.
Create helper functions such as:
is_wall(position)
is_valid_position(position)
get_neighbors(position)

ghost.py
Handle ghost-related logic.
Implement functions/classes for:
Detecting ghost positions.
Checking whether a cell is dangerous.
Avoiding ghost positions.
Optionally treating cells immediately around ghosts as higher-cost/dangerous cells.
Do NOT simply remove every cell near ghosts if doing so makes the map impossible to solve. Prefer a sensible safety mechanism.
pacman.py
Refactor the original Pac-Man implementation.
Pac-Man should:
Detect current position.
Find remaining food.
Select an appropriate target.
Call A*.
Follow the returned path.
Recalculate the path when needed.
Avoid ghosts.
Continue until all food is collected.
Food Collection Strategy
Pac-Man should not simply choose a random food item.
Implement a reasonable target-selection strategy.
For example:
Find all remaining food positions.
Calculate the distance/path cost from Pac-Man to each food.
Ignore unreachable food.
Prefer a reachable food with the lowest safe path cost.
Navigate to it.
After collecting it, repeat the process.
If ghosts are nearby, prioritize safety over shortest distance.
Ghost Avoidance
Ghost avoidance is extremely important.
A* should not intentionally select a path that moves Pac-Man directly onto a ghost.
At minimum:
Ghost position = blocked/dangerous

Preferably, also consider adjacent ghost cells as dangerous/high-cost depending on the game implementation.
If the ghost moves during execution:
Recalculate Pac-Man's path.
Do not blindly follow an old path.
If the current path becomes dangerous, immediately search for a safer path.
The program should gracefully handle situations where no safe path is currently available.
Automated Demo
Create:
demo.py

The demo must run Pac-Man automatically.
The user should be able to execute something like:
python demo.py

and watch Pac-Man solve the map without keyboard input.
The demo should:
Start automatically.
Display the game.
Automatically control Pac-Man.
Show Pac-Man moving toward food.
Avoid ghosts.
Continue until all food is collected.
Print useful information to the console.
For example:
Starting Pac-Man A* Demo...

Pac-Man position: (5, 7)
Remaining food: 12
Target food: (8, 10)
A* path found: 16 steps

Following path...

Food collected!
Remaining food: 11

Recalculating path...
...
All food collected!
Demo completed successfully.

No Keyboard Input
This is a strict requirement.
Do NOT require:
Arrow keys
WASD
Manual movement
User interaction

Pac-Man must be controlled by the algorithm.
If the original skeleton contains keyboard-control code, keep it only if necessary for optional manual mode, but the default demo must be fully autonomous.
Visualization
If possible, add a simple visual indication of the A* path.
For example:
Pac-Man = player
Food = target
Ghost = danger
Wall = blocked
A* path = visually highlighted
If modifying the original game's rendering is difficult, print/debug the path in the console instead.
Do not sacrifice functionality just to add visual effects.
Testing Requirements
Create tests for:
Test 1 — Basic A*
3×3 grid
Start → Goal

Verify that A* finds a valid path.
Test 2 — Wall avoidance
Verify that A* does not move through walls.
Test 3 — Unreachable goal
If the goal is completely blocked, verify that the algorithm handles it gracefully.
Test 4 — Ghost avoidance
Verify that Pac-Man does not intentionally select a path through a ghost.
Test 5 — Food collection
Run the complete demo and verify that all food items are collected.
Test 6 — No keyboard input
Verify that the demo can complete without any user movement input.
Code Quality Requirements
Please make the implementation:
Clean
Modular
Beginner-friendly
Well-commented
Easy to understand
PEP 8 reasonably compliant
Avoid unnecessary complexity
Avoid duplicated logic
Use meaningful variable/function/class names
Keep A* logic separate from game/UI logic
Do not introduce unnecessary frameworks.
Prefer Python standard library and the libraries already used by the original Pac-Man project.
README.md
Create a detailed README containing:
1. Project Overview
Explain what the project does.
2. A* Explanation
Explain:
What A* is.
g-cost.
h-cost.
f-cost.
Manhattan distance.
Why A* is suitable for Pac-Man.
3. Architecture
Explain each Python module.
4. How Ghost Avoidance Works
Explain the safety mechanism.
5. How Food Selection Works
Explain how Pac-Man chooses the next food.
6. Installation
Provide exact commands.
7. Running the Demo
Example:
python demo.py

8. Running Tests
Example:
python test_astar.py

9. Expected Result
Explain that Pac-Man should automatically collect all food without keyboard input.
10. Limitations
Clearly mention any limitations of the original Pac-Man skeleton or ghost behavior.
Important: Preserve Existing Functionality
Before modifying the skeleton:
Inspect the existing code.
Understand how the map, Pac-Man, food, ghosts, and rendering currently work.
Avoid breaking existing functionality unnecessarily.
Integrate A* into the existing architecture instead of rewriting everything without reason.
If the original code uses a specific library/version, maintain compatibility with it.
Final Verification
After implementation:
Run the 3×3 A* test.
Run wall avoidance test.
Run unreachable-goal test.
Run ghost avoidance test.
Run the complete Pac-Man demo.
Confirm that no keyboard input is required.
Confirm that Pac-Man can collect all food.
Fix any runtime errors.
Make sure all imports work from a clean project.
Make sure the README accurately describes how to run the project.
Do not stop after creating files. Actually test the implementation and fix errors.
At the end, provide:
Implementation completed.

Files created/modified:
- ...
- ...
- ...

How to run:
python demo.py

How to test:
python test_astar.py

Result:
- A* implemented
- Wall detection implemented
- Ghost avoidance implemented
- Automated food collection implemented
- No keyboard input required

The final result should be a working, submission-ready Phase 4 Pac-Man A Pathfinding project*, not just a code example.

This project was built with [Lovable](https://lovable.dev).

## Build with Lovable

Continue developing this project in the [Lovable editor](https://lovable.dev/projects/750c62a5-a577-4dd9-9d7f-0b031d245419).

- **Ship faster**: describe what you want to build and Lovable handles the code.
- **Stay in sync**: every change made in Lovable is committed straight to this repository.
- **Full ownership**: this code is yours. Push to `main` on GitHub and your changes sync back into Lovable, ready for your next prompt.

## Development

Prefer working locally? You need Node.js and npm — [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating).

```sh
git clone <this-repository-url>
cd <repository-name>
npm i
npm run dev
```
