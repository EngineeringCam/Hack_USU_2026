import os
import sys
import pygame

# Ensure project root (parent directory) is on sys.path so sibling packages are importable
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from world.world import World
from world.settings import MAZE_WIDTH, MAZE_LENGTH, FPS
from AI_Agents import StandardAI


def main():
    pygame.init()
    screen = pygame.display.set_mode((MAZE_WIDTH, MAZE_LENGTH))
    clock = pygame.time.Clock()

    world = World(MAZE_WIDTH, MAZE_LENGTH)

    font = pygame.font.SysFont(None, 24)

    running = True
    while running and world.running:
        # let the world collect and handle its events (including QUIT)
        world.handle_events()

        # simple fallback: also catch QUIT from the main loop event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- update
        world.update()

        # --- draw
        screen.fill((30, 30, 30))
        world.draw()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()