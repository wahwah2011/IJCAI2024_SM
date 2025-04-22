from baseagent import AbstractAgent
from typing import List, Optional
import numpy as np

class GoodAgent(AbstractAgent):
    POVERTY_THRESHOLD = 0.3

    def __init__(self):
        print("GoodAgent")
        self.is_initialized = False
        self.whoami = "good"
        self.reciprocity_score: Optional[List[float]] = None
        self.attack_history: Optional[List[float]] = None
        self.player_idx: Optional[int] = None

    def __del__(self):
        # No need for explicit delete in Python
        pass

    def play_round(self, num_players: int, num_tokens: int, player_idx: int, round_num: int,
                   received: List[float], popularities: List[float],
                   influence: List[List[float]], allocations: List[int]):
        print("GoodAgent playRound")
        if not self.is_initialized:
            self.init_reciprocity(num_players)
        self.player_idx = player_idx
        allocations[:] = [0] * num_players
        allocations[player_idx] = num_tokens

        self.poverty_relief(num_players, popularities, allocations)
        self.support_attack_victims(num_players, received, allocations)
        self.maintain_reciprocity(num_players, influence, allocations)
        self.progressive_redistribution(num_players, popularities, allocations)

        allocations[player_idx] = max(allocations[player_idx], int(num_tokens * 0.2))
        print("GoodAgent allocations:", allocations)
        print("PLAYROUND FINISHED\n")

    def post_contract(self, player_idx: int):
        pass

    def init_reciprocity(self, num_players: int):
        self.reciprocity_score = [0.0] * num_players
        self.attack_history = [0.0] * num_players
        self.is_initialized = True

    def poverty_relief(self, num_players: int, popularities: List[float], allocations: List[int]):
        print("GoodAgent povertyRelief")
        max_pop = max(popularities)
        relief_pool = int(allocations[self.player_idx] * 0.15)
        for i in range(num_players):
            if relief_pool > 0 and num_players > 0:
                if popularities[i] < self.POVERTY_THRESHOLD * max_pop:
                    allocations[i] += relief_pool // num_players
        allocations[self.player_idx] -= relief_pool
        print("GoodAgent povertyRelief finished")

    def support_attack_victims(self, num_players: int, received: List[float], allocations: List[int]):
        compensation_pool = 0
        for i in range(num_players):
            if received[i] < 0:
                self.attack_history[i] += abs(received[i])
                compensation_pool += int(abs(received[i]) * 0.5)
        allocations[self.player_idx] -= compensation_pool
        for i in range(num_players):
            if self.attack_history[i] > 0:
                allocations[i] += compensation_pool // num_players

    def maintain_reciprocity(self, num_players: int, influence: List[List[float]], allocations: List[int]):
        reciprocity_rankings = []
        for i in range(num_players):
            self.reciprocity_score[i] = 0.9 * self.reciprocity_score[i] + 0.1 * influence[i][self.player_idx]
            if i != self.player_idx:
                reciprocity_rankings.append((self.reciprocity_score[i], i))
        reciprocity_rankings.sort(reverse=True)
        reciprocity_pool = int(allocations[self.player_idx] * 0.1)
        for j in range(min(3, len(reciprocity_rankings))):
            idx = reciprocity_rankings[j][1]
            allocations[idx] += reciprocity_pool // 3
        allocations[self.player_idx] -= reciprocity_pool

    def progressive_redistribution(self, num_players: int, popularities: List[float], allocations: List[int]):
        poorest = self.get_poorest_agents(num_players, popularities, 0.5)
        redistribution = int(allocations[self.player_idx] * 0.15)
        allocations[self.player_idx] -= redistribution
        for idx in poorest:
            allocations[idx] += redistribution // len(poorest) if poorest else 0

    def get_poorest_agents(self, num_players: int, popularities: List[float], percentile: float) -> List[int]:
        rankings = sorted([(pop, i) for i, pop in enumerate(popularities)])
        count = int(num_players * percentile)
        return [rankings[i][1] for i in range(count)]
