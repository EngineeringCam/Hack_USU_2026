# Hackathon_Stealth_main/Agent_Actions/Agent_Actions.py
import math
from typing import List, Optional

from Hackathon_Stealth_main.AI_Agents.AI_Agents import StandardAI
from Hackathon_Stealth_main.utils.utils import in_vision_cone, distance, clamp
from Hackathon_Stealth_main.Vision_Cones.Cones_Initialization import draw_vision_cone

import pygame


class Agent_Actions:
    def __init__(self, show_cones: bool = False):
        self.show_cones = show_cones

    @staticmethod
    def _face_toward(agent: StandardAI, target):
        """Set agent.facing toward target (tx,ty)."""
        if hasattr(agent, "_set_facing_toward"):
            agent._set_facing_toward(target)
        elif hasattr(agent, "set_facing_toward"):
            agent.set_facing_toward(target)
        else:
            tx, ty = float(target[0]), float(target[1])
            dx = tx - agent.x
            dy = ty - agent.y
            nx, ny = agent._normalize(dx, dy)
            if nx is not None:
                agent.facing = (nx, ny)

    def move_agents(self, agents: List[StandardAI], player, maze, dt: float = 1.0):
        """
        Move agents with maze collision:
        - axis-separated movement (X, then Y) to avoid corner-through.
        - agents: list of StandardAI
        - player: object with .x and .y
        - maze: Maze instance (must have is_wall_at_pixel, width, height, tile_size)
        - dt: seconds
        """
        if dt <= 0:
            return

        for a in agents:
            vx = 0.0
            vy = 0.0

            # chase
            if in_vision_cone(a, player, maze):
                a.chasing = True
                dx = player.x - a.x
                dy = player.y - a.y
                nx, ny = a._normalize(dx, dy)
                if nx is not None:
                    a.facing = (nx, ny)
                    speed = float(getattr(a, "running_speed", 0.0))
                    vx = nx * speed
                    vy = ny * speed

            else:
                # lost sight -> resume patrol
                if getattr(a, "chasing", False):
                    a.chasing = False
                    if a.patrol_endA is None or a.patrol_endB is None:
                        a.patrol_target = a.patrol_endA or a.patrol_endB
                    else:
                        dA = math.hypot(a.patrol_endA[0] - a.x, a.patrol_endA[1] - a.y)
                        dB = math.hypot(a.patrol_endB[0] - a.x, a.patrol_endB[1] - a.y)
                        a.patrol_target = a.patrol_endA if dA < dB else a.patrol_endB
                        self._face_toward(a, a.patrol_target)

                # patrol
                if a.patrol_target is None:
                    a.patrol_target = a.patrol_endA if a.patrol_endA is not None else a.patrol_endB

                if a.reached_patrol_target():
                    if a.patrol_target == a.patrol_endA:
                        a.patrol_target = a.patrol_endB
                    else:
                        a.patrol_target = a.patrol_endA
                    if a.patrol_target is not None:
                        self._face_toward(a, a.patrol_target)

                if a.patrol_target is not None:
                    tx, ty = a.patrol_target
                    dx = tx - a.x
                    dy = ty - a.y
                    nx, ny = a._normalize(dx, dy)
                    if nx is not None:
                        a.facing = (nx, ny)
                        speed = float(getattr(a, "standard_speed", 0.0))
                        vx = nx * speed
                        vy = ny * speed

            # apply axis-separated movement and collision
            move_x = vx * dt
            a.x += move_x
            if a._collides_with_wall(maze):
                a.x -= move_x

            move_y = vy * dt
            a.y += move_y
            if a._collides_with_wall(maze):
                a.y -= move_y

            # clamp within maze pixel bounds (top-left coordinates)
            size = getattr(a, "size", 1)
            a.x = clamp(a.x, 0, max(0, maze.width - size))
            a.y = clamp(a.y, 0, max(0, maze.height - size))

    def draw_agents(self, screen: pygame.Surface, agents: List[StandardAI], draw_cones: Optional[bool] = None):
        if draw_cones is None:
            draw_cones = self.show_cones

        for a in agents:
            size = getattr(a, "size", 6)
            cx = int(a.x + size / 2)
            cy = int(a.y + size / 2)
            pygame.draw.circle(screen, (20, 150, 20), (cx, cy), max(2, size // 2))

            if draw_cones:
                try:
                    draw_vision_cone(a, screen, color=(255, 255, 0))
                except Exception:
                    pass