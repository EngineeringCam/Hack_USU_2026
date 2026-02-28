import math

def distance(a, b):
        return math.hypot(a.x - b.x, a.y - b.y)

def clamp(val, low, high):
        return max(low, min(high, val))

def in_vision_cone(agent, target, maze):
    # --- 1) Distance check (squared, fast)
    dx = target.x - agent.x
    dy = target.y - agent.y

    dist_sq = dx * dx + dy * dy
    max_dist_sq = agent.vision_distance * agent.vision_distance

    if dist_sq == 0 or dist_sq > max_dist_sq:
        return False

    # --- 2) Angle check (dot product)
    inv_dist = 1 / math.sqrt(dist_sq)
    to_target_x = dx * inv_dist
    to_target_y = dy * inv_dist

    dot = (
        agent.facing[0] * to_target_x +
        agent.facing[1] * to_target_y
    )

    if dot < agent.cos_half_vision:
        return False

    # --- 3) Line-of-sight wall check (only if above passes)

    # Use agent center
    ax = agent.x + agent.size / 2
    ay = agent.y + agent.size / 2

    # Use target center (player likely already center-based)
    tx = target.x
    ty = target.y

    # Ray march with fixed step size (fast & stable)
    steps = int(math.sqrt(dist_sq) // 6)  # 6px step = good balance

    if steps <= 1:
        return True

    step_x = (tx - ax) / steps
    step_y = (ty - ay) / steps

    px = ax
    py = ay

    for _ in range(steps):
        px += step_x
        py += step_y
        if maze.is_wall_at_pixel(px, py):
            return False

    return True