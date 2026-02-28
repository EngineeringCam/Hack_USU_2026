# states/playing_state.py
import pygame

from states.base_state import BaseState
from world.maze import Maze
from entities.player import Player


class PlayingState(BaseState):
    def __init__(self):

        self.grid = [[1,1,1,1,1,1,1,1],
          [1,0,1,1,1,1,1,1],
          [1,0,0,0,0,0,0,1],
          [1,0,1,1,1,1,1,1],
          [1,0,1,1,1,1,1,1],
          [1,0,1,1,1,1,1,1],
          [1,0,1,1,1,1,1,1],
          [1,1,1,1,1,1,1,1]]

        self.tile_size = 80

        # World + entities
        self.maze = Maze(self.grid, self.tile_size)

        # Start position in pixels (example: tile (1,1))
        start_x = 1 * self.tile_size
        start_y = 1 * self.tile_size
        self.player = Player(start_x, start_y, size=14, speed=180)

        # Optional: a font for debug text/UI
        self.font = None

    def handle_events(self, game, event):
        # Discrete actions only (NOT continuous movement)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Later you can switch to PauseState here
                # game.change_state(PauseState(...))
                pass

            if event.key == pygame.K_r:
                # Simple restart: re-init this state
                game.change_state(PlayingState())

    def update(self, game, dt):
        # Smooth movement uses held keys each frame
        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += 1

        # Tell the player to move, passing the maze for collision checks
        self.player.update(dt, self.maze, dx, dy)

        # Optional: win check if your Maze supports it
        # if self.maze.is_goal_pixel(self.player.x, self.player.y):
        #     game.change_state(WinState())

    def draw(self, game, screen):
        # Draw static world (ideally pre-rendered in Maze)
        self.maze.draw(screen)

        # Draw dynamic entity
        self.player.draw(screen)

        # Optional: quick debug overlay
        # if self.font is None:
        #     self.font = pygame.font.SysFont(None, 24)
        # txt = self.font.render("WASD/Arrows to move. R to restart.", True, (255, 255, 255))
        # screen.blit(txt, (10, 10))