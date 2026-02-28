# Hackathon_Stealth_main/AI_Agents/AI_Agents.py
import math
import random
import pygame
# don't import draw_vision_cone here unless you actually draw from AI file

class StandardAI:
    def __init__(self, x, y, size=6):
        # position is top-left of a square hitbox (consistent with Player)
        self.x = float(x)
        self.y = float(y)

        # small square hitbox size (pixels)
        self.size = int(size)

        # facing as a normalized vector (dx, dy). Must be non-zero.
        self.facing = (1.0, 0.0)

        # vision parameters
        self.vision_distance = 120.0
        self.vision_angle = math.pi / 2  # 90 degrees

        # speeds in pixels per second (tweak to taste)
        self.standard_speed = 60.0
        self.running_speed = 180.0

        # runtime state
        self.chasing = False
        self.patrol_endA = None   # (x,y) in pixels (top-left or center consistent with how you use them)
        self.patrol_endB = None
        self.patrol_target = None
        self.cos_half_vision = math.cos(self.vision_angle / 2)

    def get_rect(self):
        """Return a pygame.Rect representing the agent's hitbox (top-left coords)."""
        return pygame.Rect(int(self.x), int(self.y), int(self.size), int(self.size))

    def _collides_with_wall(self, maze):
        """
        Check collision against maze walls using tile lookup (same method Player uses).
        This doesn't require Maze.is_wall_at_pixel to exist.
        """
        rect = self.get_rect()

        # Determine which tiles the agent overlaps
        left_tile = rect.left // maze.tile_size
        right_tile = (rect.right - 1) // maze.tile_size
        top_tile = rect.top // maze.tile_size
        bottom_tile = (rect.bottom - 1) // maze.tile_size

        for row in range(int(top_tile), int(bottom_tile) + 1):
            for col in range(int(left_tile), int(right_tile) + 1):
                # Bounds check: outside map counts as wall
                if row < 0 or row >= maze.rows or col < 0 or col >= maze.cols:
                    return True

                # If tile value 1 is wall (your convention), collide
                if maze.grid[row][col] == 1:
                    return True

        return False

    @classmethod
    def on_track(cls, endA, endB, random_t=None, size=6):
        """
        Create an agent located on the segment endA->endB at random_t in [0,1].
        endA/endB should be pixel (x,y) points.
        """
        if random_t is None:
            random_t = random.random()

        ax, ay = float(endA[0]), float(endA[1])
        bx, by = float(endB[0]), float(endB[1])

        x = ax + (bx - ax) * random_t
        y = ay + (by - ay) * random_t

        agent = cls(x, y, size=size)
        agent.patrol_endA = (ax, ay)
        agent.patrol_endB = (bx, by)
        agent.patrol_target = random.choice([agent.patrol_endA, agent.patrol_endB])
        agent._set_facing_toward(agent.patrol_target)
        return agent

    def _set_facing_toward(self, target):
        """Internal helper: set facing vector toward target (tx,ty)."""
        tx, ty = float(target[0]), float(target[1])
        dx = tx - self.x
        dy = ty - self.y
        nx, ny = self._normalize(dx, dy)
        if nx is not None:
            self.facing = (nx, ny)

    # public alias kept for compatibility
    def set_facing_toward(self, target):
        self._set_facing_toward(target)

    @staticmethod
    def _normalize(dx, dy):
        mag = math.hypot(dx, dy)
        if mag == 0:
            return (None, None)
        return (dx / mag, dy / mag)

    def reached_patrol_target(self, thresh=4.0):
        """Return True if agent is within thresh pixels of patrol_target."""
        if self.patrol_target is None:
            return False
        tx, ty = self.patrol_target
        return math.hypot(tx - self.x, ty - self.y) <= thresh


# Keep the wrapper subclass if you previously had one (optional)
class StandardAI(StandardAI):
    def __init__(self, x, y, size=6):
        super().__init__(x, y, size=size)
        self.cos_half_vision = math.cos(self.vision_angle / 2)