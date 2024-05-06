from baseagent import AbstractAgent

import numpy as np

class ScriptAgent(AbstractAgent):

    def __init__(self, _me, _numAgents, _numRounds, _thePlan):
        super().__init__()
        self.whoami = "scripted"
        self.me = _me
        self.numAgents = _numAgents
        self.thePlan = _thePlan
        self.gameParams = {}

    def setGameParams(self, gameParams, visualTraits):
        self.gameParams = gameParams

    def play_round(self, player_idx, round_num, recieved, popularities, influence, extra_data):
        allocations = np.zeros(len(popularities), dtype=int)
        for i in range(0, self.numAgents):
            allocations[i+1] = self.thePlan[round_num][self.me][i]

        return allocations
