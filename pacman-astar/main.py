"""Pygame rendering for the autonomous Pac-Man.

Run `python main.py` (or `python demo.py`) to watch Pac-Man play. There is
no keyboard control: every move comes from the A* planner. The only key
handled is ESC / window close, which quits the window.
"""

import sys

import pygame

import config
from pacman import Game


def grid_to_pixels(position):
    """Convert a grid cell to the pixel position of its centre."""
    x, y = position
    half = config.CELL_SIZE // 2
    return (x * config.CELL_SIZE + half, y * config.CELL_SIZE + half)


def draw_grid(screen, game):
    """Draw walls, food, the planned A* path, ghosts and Pac-Man."""
    grid = game.grid
    size = config.CELL_SIZE

    screen.fill(config.COLOR_BACKGROUND)

    # Walls
    for (x, y) in grid.walls:
        pygame.draw.rect(screen, config.COLOR_WALL,
                         (x * size, y * size, size, size), border_radius=4)

    # A* path highlight
    for cell in game.pacman.path:
        pygame.draw.circle(screen, config.COLOR_PATH, grid_to_pixels(cell), 3)

    # Food
    for cell in grid.food:
        pygame.draw.circle(screen, config.COLOR_FOOD, grid_to_pixels(cell), 3)

    # Current target
    if game.pacman.target is not None:
        pygame.draw.circle(screen, config.COLOR_TARGET,
                           grid_to_pixels(game.pacman.target), size // 3, 2)

    # Ghosts
    for position in game.ghosts.positions():
        px, py = grid_to_pixels(position)
        pygame.draw.circle(screen, config.COLOR_GHOST, (px, py), size // 2 - 2)

    # Pac-Man
    pygame.draw.circle(screen, config.COLOR_PACMAN,
                       grid_to_pixels(game.pacman.position), size // 2 - 2)


def draw_hud(screen, font, game):
    """Draw the score / remaining-food text under the maze."""
    text = "Score: {}   Food left: {}   Target: {}".format(
        game.pacman.score, game.remaining_food(), game.pacman.target)
    if game.won:
        text = "All food collected!  Final score: {}".format(game.pacman.score)
    label = font.render(text, True, config.COLOR_TEXT)
    screen.blit(label, (8, config.CELL_SIZE * game.grid.height + 10))


def run(verbose=True, max_frames=config.MAX_DEMO_STEPS):
    """Open the window and let Pac-Man play until all food is collected."""
    pygame.init()
    game = Game()
    width = game.grid.width * config.CELL_SIZE
    height = game.grid.height * config.CELL_SIZE + config.HUD_HEIGHT
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pac-Man A* (fully automatic)")
    font = pygame.font.SysFont("monospace", 16)
    clock = pygame.time.Clock()

    frames = 0
    running = True
    while running and frames < max_frames:
        frames += 1
        for event in pygame.event.get():
            # Only window management -- no gameplay input at all.
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        if not game.finished:
            info = game.step()
            if verbose and (info.get("ate") or info.get("replanned")):
                print("pos={} food_left={} target={} path={}".format(
                    game.pacman.position, game.remaining_food(),
                    game.pacman.target, len(game.pacman.path)))

        draw_grid(screen, game)
        draw_hud(screen, font, game)
        pygame.display.flip()
        clock.tick(config.FPS)

        if game.finished:
            pygame.time.wait(1500)
            running = False

    pygame.quit()
    return game


if __name__ == "__main__":
    finished_game = run()
    sys.exit(0 if finished_game.won else 1)
