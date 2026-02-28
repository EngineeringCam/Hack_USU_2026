import sys
import pygame
from world import World
from settings import MAZE_WIDTH, MAZE_LENGTH, FPS
from AI_Agents import StandardAI

class main():
    pygame.init()
    screen = pygame.display.set_mode((MAZE_WIDTH, MAZE_LENGTH))
    clock = pygame.time.Clock()

    world = World()
    world.populate()

    font = pygame.font.SysFont(None, 24)

    running = True
    while running:
        for event in pygame.event.get():
            running = False

        # --- update
        world.update()

        # --- draw
        screen.fill((30, 30, 30))
        world.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

    if __name__ == "__main__":
        main()