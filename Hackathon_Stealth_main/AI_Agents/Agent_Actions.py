import math
from typing import List, Optional

# Relative imports inside package
from ..AI_Agents.AI_Agents import StandardAI
from ..utils.utils import in_vision_cone, distance, clamp
from ..Vision_Cones.Cones_Initialization import draw_vision_cone

import pygame


class Agent_Actions:
    """
    Controls AI agent updates: patrolling between two endpoints and chasing
    the player when inside vision cone. Movement is applied axis-by-axis
    and checked against the Maze to prevent walking through walls.
    """

    def __init__(self, show_cones: bool = False):
        # toggle debug drawing of vision cones
        self.show_cones = show_cones

    # small helper to call whichever facing method exists on the agent
    @staticmethod
    def _face_toward(agent: StandardAI, target):
        """Set agent.facing toward target (tx,ty). Tries available helper names."""
        if hasattr(agent, "set_facing_toward"):
            agent.set_facing_toward(target)
        elif hasattr(agent, "_set_facing_toward"):
            agent._set_facing_toward(target)
        else:
            # fallback: compute normalized vector directly
            tx, ty = float(target[0]), float(target[1])
            dx = tx - agent.x
            dy = ty - agent.y
            nx, ny = agent._normalize(dx, dy)
            if nx is not None:
                agent.facing = (nx, ny)

    def move_agents(self, agents: List[StandardAI], player, maze, dt: float = 1.0):
        """
        Update and move agents for a single frame.
        - agents: list of StandardAI instances
        - player: object with .x and .y
        - maze: Maze instance (must provide is_wall_at_pixel(x,y), width, height)
        - dt: seconds since last update (float)
        """
        if dt <= 0:
            return

        for a in agents:
            # --- Decide desired velocity (vx, vy) in pixels/sec ---
            vx = 0.0
            vy = 0.0

            # 1) If sees player, chase
            if in_vision_cone(a, player):
                a.chasing = True

                # face player and set velocity
                dx = player.x - a.x
                dy = player.y - a.y
                nx, ny = a._normalize(dx, dy)
                if nx is not None:
                    a.facing = (nx, ny)
                    speed = float(getattr(a, "running_speed", 0.0))
                    vx = nx * speed
                    vy = ny * speed

            else:
                # 2) Lost sight -> if was chasing, pick nearest patrol endpoint and resume patrol
                if getattr(a, "chasing", False):
                    a.chasing = False
                    # choose nearest endpoint as patrol target
                    if a.patrol_endA is None or a.patrol_endB is None:
                        # nothing to patrol to
                        a.patrol_target = a.patrol_endA or a.patrol_endB
                    else:
                        dA = math.hypot(a.patrol_endA[0] - a.x, a.patrol_endA[1] - a.y)
                        dB = math.hypot(a.patrol_endB[0] - a.x, a.patrol_endB[1] - a.y)
                        a.patrol_target = a.patrol_endA if dA < dB else a.patrol_endB
                        self._face_toward(a, a.patrol_target)

                # 3) Patrol behavior
                if a.patrol_target is None:
                    # default target if missing
                    a.patrol_target = a.patrol_endA if a.patrol_endA is not None else a.patrol_endB

                # If reached target, switch to other end
                if a.reached_patrol_target():
                    if a.patrol_target == a.patrol_endA:
                        a.patrol_target = a.patrol_endB
                    else:
                        a.patrol_target = a.patrol_endA
                    if a.patrol_target is not None:
                        self._face_toward(a, a.patrol_target)

                # move toward patrol target
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

            # --- Apply movement with axis-separated collision checks ---
            # X axis
            move_x = vx * dt
            a.x += move_x
            collided_x = False
            if hasattr(a, "_collides_with_wall"):
                if a._collides_with_wall(maze):
                    collided_x = True
                    a.x -= move_x
            else:
                # fallback: check corners using maze helper if available
                if maze is not None and hasattr(maze, "is_wall_at_pixel"):
                    # check four corners of agent rect (top-left semantics)
                    rect = getattr(a, "get_rect")() if hasattr(a, "get_rect") else None
                    if rect is None:
                        # assume small square centered at (x,y) - try top-left
                        corners = [
                            (int(a.x), int(a.y)),
                            (int(a.x + getattr(a, "size", 1) - 1), int(a.y)),
                            (int(a.x), int(a.y + getattr(a, "size", 1) - 1)),
                            (int(a.x + getattr(a, "size", 1) - 1), int(a.y + getattr(a, "size", 1) - 1)),
                        ]
                    else:
                        corners = [
                            (rect.left, rect.top),
                            (rect.right - 1, rect.top),
                            (rect.left, rect.bottom - 1),
                            (rect.right - 1, rect.bottom - 1),
                        ]
                    for (px, py) in corners:
                        if maze.is_wall_at_pixel(px, py):
                            collided_x = True
                            break
                    if collided_x:
                        a.x -= move_x

            # Y axis
            move_y = vy * dt
            a.y += move_y
            collided_y = False
            if hasattr(a, "_collides_with_wall"):
                if a._collides_with_wall(maze):
                    collided_y = True
                    a.y -= move_y
            else:
                # fallback: corner checks
                if maze is not None and hasattr(maze, "is_wall_at_pixel"):
                    rect = getattr(a, "get_rect")() if hasattr(a, "get_rect") else None
                    if rect is None:
                        corners = [
                            (int(a.x), int(a.y)),
                            (int(a.x + getattr(a, "size", 1) - 1), int(a.y)),
                            (int(a.x), int(a.y + getattr(a, "size", 1) - 1)),
                            (int(a.x + getattr(a, "size", 1) - 1), int(a.y + getattr(a, "size", 1) - 1)),
                        ]
                    else:
                        corners = [
                            (rect.left, rect.top),
                            (rect.right - 1, rect.top),
                            (rect.left, rect.bottom - 1),
                            (rect.right - 1, rect.bottom - 1),
                        ]
                    for (px, py) in corners:
                        if maze.is_wall_at_pixel(px, py):
                            collided_y = True
                            break
                    if collided_y:
                        a.y -= move_y

            # --- Clamp inside the map bounds as a final safety net ---
            if maze is not None:
                size = getattr(a, "size", 1)
                a.x = clamp(a.x, 0, max(0, maze.width - size))
                a.y = clamp(a.y, 0, max(0, maze.height - size))

    def draw_agents(self, screen: pygame.Surface, agents: List[StandardAI], draw_cones: Optional[bool] = None):
        """
        Draw agents as small circles and optionally their vision cones for debugging.
        - screen: pygame.Surface
        - agents: list of agents
        - draw_cones: overrides self.show_cones if not None
        """
        if draw_cones is None:
            draw_cones = self.show_cones

        for a in agents:
            # draw agent (centered on top-left coordinates if that's how agent.x/y are used)
            size = getattr(a, "size", 6)
            # If agent.x/y are top-left, draw centered for nicer visuals:
            cx = int(a.x + size / 2)
            cy = int(a.y + size / 2)
            pygame.draw.circle(screen, (20, 150, 20), (cx, cy), max(2, size // 2))

            if draw_cones:
                # draw vision cone outline (function expects agent and screen)
                try:
                    draw_vision_cone(a, screen, color=(255, 255, 0))
                except Exception:
                    # ignore drawing errors in debug mode
                    pass