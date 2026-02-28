import pygame
import math

def draw_vision_cone(agent, screen, color=(255,255,0)):
    steps = max(3, int(agent.vision_angle * 10))  # scale detail with angle
    base_angle = math.atan2(agent.facing[1], agent.facing[0])

    points = [(agent.x, agent.y)]
    for i in range(steps + 1):
        a = base_angle - agent.vision_angle/2 + i * agent.vision_angle / steps
        x = agent.x + agent.vision_distance * math.cos(a)
        y = agent.y + agent.vision_distance * math.sin(a)
        points.append((x, y))

    pygame.draw.polygon(screen, color, points, 1)