import math
import random
from ..Vision_Cones import draw_vision_cones

class StandardAI:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

        # facing as a normalized vector (dx, dy). Must be non-zero
        self.facing = (1.0, 0.0)

        # vision parameters
        self.vision_distance = 120.0
        self.vision_angle = math.pi /2 # 90 degrees

        self.standard_speed = 1
        self.running_speed = 3

        self.chasing = False
        self.patrol_endA = None # tuple (x, y)
        self.patrol_endB = None # tuple (x, y)
        self.patrol_target = None # current target point (x, y)
        self.cos_half_vision = math.cos(self.vision_angle / 2)

    @classmethod
    def on_track(cls, endA, endB, random_t=None):
        """
        Factory: create an agent at a random spot on the segment endA->endB.
        - endA, endB: (x, y)
        random_t: optional float in [0,1] to pick position; if None, chosen randomly.
        The agent faces randomly toward endA or endB initially and will patrol.
        """
        if random_t is None:
            random_t = random.random()

        ax, ay = float(endA[0]), float(endA[1])
        bx, by = float(endB[0]), float(endB[1])

        # position along segment
        x = ax + (bx - ax) * random_t
        y = ay + (by - ay) * random_t

        agent = cls(x, y)
        agent.patrol_endA = (ax, ay)
        agent.patrol_endB = (bx, by)

        # pick a random end to face / move toward first
        first_target = random.choice(['A', 'B'])
        if first_target == 'A':
            agent.patrol_target = agent.patrol_endA
        else:
            agent.patrol_target = agent.patrol_endB

        # set facing to point toward chosen end
        agent._set_facing_toward(agent.patrol_target)

        return agent
    
    def set_facing_toward(self, target):
        """Set facing to a normalized vector toward target (tx,ty)."""
        tx, ty = float(target[0]), float(target[1])
        dx = tx - self.x
        dy = ty - self.y
        nx, ny = self._normalize(dx, dy)
        # if zero-length, keep existing facing
        if nx is not None:
            self.facing = (nx, ny)

    @staticmethod
    def _normalize(dx, dy):
        mag = math.hypot(dx, dy)
        if mag == 0:
            return (None, None)
        return (dx / mag, dy / mag)
    
    def reached_patrol_target(self, thresh=4.0):
        """Return True if agent is near patrol_target (theshold in game units)."""
        if self.patrol_target is None:
            return False
        tx, ty = self.patrol_target
        return math.hypot(tx - self.x, ty - self.y) <= thresh



class StandardAI(StandardAI):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.cos_half_vision = math.cos(self.vision_angle / 2)