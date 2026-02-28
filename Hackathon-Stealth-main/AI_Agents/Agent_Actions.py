from AI_Agents import StandardAI
from ..utils.utils import in_vision_cone, distance

class Agent_Actions:
    def move_agents(self, StandardAI, player):
        self.AI = StandardAI
        self.player = player

        for c in self.AI:
            target = None
            
            for AI in self.AI:
                if in_vision_cone(c, player):
                    target = player
                else:
                    target = None