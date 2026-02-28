import math
from AI_Agents import StandardAI
from ..utils.utils import in_vision_cone, distance
from ..Vision_Cones import draw_vision_cones

class Agent_Actions:
    def move_agents(self, agents, player, dt=1.0):
        """
        Move a list of StandardAI agents for one frame.
        - agents: list of StandardAI instances
        - player: object with .x and .y
        - dt: seconds since last update (use 1.0 if you don't have dt).
        """
        for a in agents:
            # 1) If sees player, chase
            if in_vision_cone(a, player):
                a.chasing = True
                # face the player
                dx = player.x - a.x
                dy = player.y - a.y
                nx, ny = StandardAI._normalize(dx, dy)
                if nx is not None:
                    a.facing = (nx, ny)

                # move toward player at running speed
                move_dist = a.running_speed * dt
                dist_to_player = math.hypot(dx, dy)
                if dist_to_player <= move_dist or dist_to_player == 0:
                    # reach player position (snap)
                    a.x = player.x
                    a.y = player.y
                else:
                    a.x += nx * move_dist
                    a.y += ny * move_dist

            else:
                # 2) No Longer sees the player -> stop chasing and resume patrol
                if a.chasing:
                    a.chasing = False
                    # choose nearest patrol endpoint as next patrol target
                    dA = math.hypot(a.patrol_endA[0] - a.x, a.patrol_endA[1] - a.y)
                    dB = math.hypot(a.patrol_endB[0] - a.x, a.patrol_endB[1] - a.y)
                    a.patrol_target = a.patrol_endA if dA < dB else a.patrol_endB
                    a._set_facing_toward(a.patrol_target)
        self.AI = StandardAI
        self.player = player

        # 3) Patrol behavior
        # make sure we have patrol targets set
        if a.patrol_target is None:
            # default to endA
            a.patrol_target = a.patrol_endA

        # if reached target, switch to the other end
        if a.reached_patrol_target():
            if a.patrol_target == a.patrol_endA:
                a.patrol_target = a.patrol_endB
            else:
                a.patrol_target = a.patrol_endA
            a._set_facing_toward(a.patrol_target)

        # move toward patrol target at standard speed
        tx, ty = a.patrol_target
        dx = tx - a.x
        dy = ty - a.y
        nx, ny = StandardAI._normalize(dx, dy)
        if nx is not None:
            a.facing = (nx, ny)
            move_dist = a.standard_speed * dt
            dist_to_target = math.hypot(dx, dy)
            if dist_to_target <= move_dist or dist_to_target == 0:
                # snap to target
                a.x = tx
                a.y = ty
            else:
                a.x += nx * move_dist
                a.y += ny * move_dist