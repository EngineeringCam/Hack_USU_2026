import pygame
import random

from .settings import AGENT_COUNT, MAZE_WIDTH, MAZE_LENGTH
from Hackathon_Stealth_main.Vision_Cones.Cones_Initialization import draw_vision_cone
from states.playing_state import PlayingState
from Hackathon_Stealth_main.AI_Agents.AI_Agents import StandardAI


class World:
    """
    Owns the pygame window, clock, and delegates behavior to the active State.
    """

    def __init__(self, width: int, height: int, caption: str = "Maze Game", fps: int = 60):
        # Window / timing
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)

        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = True

        # FSM: start in Playing for now
        self.current_state = PlayingState()

        self.agents = []

    def populate(self):
        """
        Create AGENT_COUNT agents placed on floor tiles (tile centers).
        Agents are added to self.agents and given two random patrol endpoints
        chosen from floor tiles. This uses the maze found on the current_state.
        """
        # don't repopulate if already have agents
        if len(self.agents) > 0:
            return

        # ensure the current state has a maze
        maze = getattr(self.current_state, "maze", None)
        if maze is None:
            # nothing to base spawn locations on
            return

        # collect floor tile coordinates (row, col)
        floor_tiles = []
        for r in range(maze.rows):
            for c in range(maze.cols):
                if maze.grid[r][c] == 0:  # floor
                    floor_tiles.append((r, c))

        if not floor_tiles:
            return

        from Hackathon_Stealth_main.AI_Agents.AI_Agents import StandardAI

        for _ in range(AGENT_COUNT):
            # pick a random floor tile for spawn
            row, col = random.choice(floor_tiles)
            center_x = col * maze.tile_size + maze.tile_size / 2
            center_y = row * maze.tile_size + maze.tile_size / 2

            # agent size (tweak if necessary)
            agent_size = 6

            # top-left coords for agent such that it's centered on tile
            top_left_x = center_x - agent_size / 2
            top_left_y = center_y - agent_size / 2

            agent = StandardAI(top_left_x, top_left_y, size=agent_size)

            # pick two random floor tiles as patrol endpoints (could be same tile)
            rA, cA = random.choice(floor_tiles)
            rB, cB = random.choice(floor_tiles)
            ax = cA * maze.tile_size + maze.tile_size / 2 - agent_size / 2
            ay = rA * maze.tile_size + maze.tile_size / 2 - agent_size / 2
            bx = cB * maze.tile_size + maze.tile_size / 2 - agent_size / 2
            by = rB * maze.tile_size + maze.tile_size / 2 - agent_size / 2

            agent.patrol_endA = (ax, ay)
            agent.patrol_endB = (bx, by)
            agent.patrol_target = random.choice([agent.patrol_endA, agent.patrol_endB])
            agent._set_facing_toward(agent.patrol_target)

            self.agents.append(agent)

    def change_state(self, new_state) -> None:
        """Switch to a new state object (e.g., MenuState(), PauseState())."""
        self.current_state = new_state

    def handle_events(self) -> None:
        """Collect pygame events and forward them to the current state."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            # Let the active state respond to events (keys, mouse, etc.)
            if self.current_state is not None:
                self.current_state.handle_events(self, event)

    def update(self) -> float:
        """
        Tick the clock and update the current state.
        Returns dt in seconds.
        """
        dt_seconds = self.clock.tick(self.fps) / 1000.0

        if self.current_state is not None:
            self.current_state.update(self, dt_seconds)

        return dt_seconds

    def draw(self) -> None:
        """Clear the screen, ask the state to draw, then present the frame."""
        self.screen.fill((0, 0, 0))

        if self.current_state is not None:
            self.current_state.draw(self, self.screen)

        pygame.display.flip()

    def drawAgents(self, screen):
        for agent in self.agents:
            pygame.draw.circle(screen, (20, 150, 20), (int(agent.x), int(agent.y)), 3)
            draw_vision_cone