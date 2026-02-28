# states/playing_state.py
import pygame
from typing import Optional

from states.base_state import BaseState
from world.maze import Maze
from entities.player import Player
from Hackathon_Stealth_main.AI_Agents.Agent_Actions import Agent_Actions


class PlayingState(BaseState):
    """
    Playing state: contains the maze, player, and drives agent updates via Agent_Actions.
    The World object (passed as 'game' to update/draw) owns the agents list; this state
    will make sure agents exist (calls game.populate()) and will move/draw them each frame.
    """

    def __init__(self):
        # grid: 16 rows x 16 cols (1 = wall, 0 = floor)
        self.grid = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1],
            [1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1],
            [1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1],
            [1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1],
            [1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
            [1,0,0,0,0,1,1,1,1,1,0,1,1,1,1,1],
            [1,0,1,1,0,0,0,0,1,1,0,1,1,1,1,1],
            [1,0,1,1,1,1,1,0,0,0,0,1,1,1,1,1],
            [1,0,1,1,1,1,1,0,1,1,0,0,0,0,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1],
            [1,0,1,0,1,0,1,0,1,1,1,1,1,0,1,1],
            [1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,1],
            [1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        ]

        self.tile_size = 50

        # Maze and Player
        self.maze = Maze(self.grid, self.tile_size)

        # Start position in pixels (tile (1,1) approx.)
        start_x = 60
        start_y = 60
        self.player = Player(start_x, start_y, size=10, speed=180)

        # Agent action controller (draw_cones True for debug)
        self.actions = Agent_Actions(show_cones=True)

        # Optional font for debug text/UI
        self.font: Optional[pygame.font.Font] = None

    def handle_events(self, game, event):
        # Discrete actions only (NOT continuous movement)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Placeholder: could switch to PauseState later
                pass

            if event.key == pygame.K_r:
                # Restart: re-create state and repopulate agents in the World
                # Clear existing agents, replace current state and repopulate
                try:
                    # clear the world's agents list if present
                    if hasattr(game, "agents"):
                        game.agents.clear()
                except Exception:
                    pass

                game.change_state(PlayingState())
                # populate will use the new current_state (this) to access maze
                if hasattr(game, "populate"):
                    game.populate()

    def update(self, game, dt):
        """
        Called each frame with the world (game) object and dt (seconds)
        - Move the player with keyboard input
        - Ensure agents exist (game.populate()) and move them with Agent_Actions
        """
        # Smooth movement (held keys)
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

        # Player movement (maze collision handled in Player.update)
        self.player.update(dt, self.maze, dx, dy)

        # Ensure the world has agents (World.populate uses current_state.maze)
        if not hasattr(game, "agents") or len(game.agents) == 0:
            if hasattr(game, "populate"):
                game.populate()

        # Move agents: game.agents is owned by the World object (game)
        if hasattr(game, "agents"):
            # pass the maze instance (this state's maze) to collision-check agents
            self.actions.move_agents(game.agents, self.player, self.maze, dt)

    def draw(self, game, screen):
        """Draw the maze, player, agents, and optional debug overlays."""
        # Draw static maze
        self.maze.draw(screen)

        # Draw player
        self.player.draw(screen)

        # Draw agents (if the world has them)
        if hasattr(game, "agents") and len(game.agents) > 0:
            self.actions.draw_agents(screen, game.agents)

        # Optional debug overlay text
        # (uncomment if you want simple on-screen instructions)
        # if self.font is None:
        #     self.font = pygame.font.SysFont(None, 20)
        # txt = self.font.render("WASD/Arrows to move. R to restart.", True, (255,255,255))
        # screen.blit(txt, (8, 8))