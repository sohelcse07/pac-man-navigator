"""Automated demo: `python demo.py`.

Pac-Man plays completely on its own. The demo tries to open a pygame
window; if no display is available (for example on a server) it falls back
to a headless run and prints the progress to the console.

Options:
    python demo.py            graphical demo (falls back to headless)
    python demo.py --headless force the console-only simulation
"""

import sys

import config
from pacman import Game


def run_headless(verbose=True, max_steps=config.MAX_DEMO_STEPS, seed=7):
    """Run the whole game without any window and print what happens."""
    game = Game(seed=seed)
    if verbose:
        print("Starting Pac-Man A* Demo...\n")
        print("Pac-Man position: {}".format(game.pacman.position))
        print("Remaining food: {}\n".format(game.remaining_food()))

    steps = 0
    last_target = None
    while not game.finished and steps < max_steps:
        steps += 1
        info = game.step()

        if verbose and info.get("target") and info["target"] != last_target:
            last_target = info["target"]
            print("Target food: {}".format(last_target))
            print("A* path found: {} steps".format(len(game.pacman.path) + 1))
            print("Following path...")

        if verbose and info.get("ate"):
            print("Food collected at {}! Remaining food: {}\n".format(
                game.pacman.position, game.remaining_food()))

        if verbose and info.get("stuck"):
            print("No safe path right now - waiting and recalculating...")

    if verbose:
        if game.won:
            print("All food collected!")
            print("Demo completed successfully in {} steps. Score: {}".format(
                steps, game.pacman.score))
        else:
            print("Demo stopped after {} steps with {} food left.".format(
                steps, game.remaining_food()))
    return game


def main():
    headless = "--headless" in sys.argv
    if not headless:
        try:
            import main as ui  # imported lazily so headless mode needs no display
            return ui.run()
        except Exception as error:      # no display, missing driver, ...
            print("Graphical mode unavailable ({}). Running headless.\n"
                  .format(error))
    return run_headless()


if __name__ == "__main__":
    game = main()
    sys.exit(0 if game.won else 1)
