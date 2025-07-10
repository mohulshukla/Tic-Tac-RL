import numpy as np
from backend.helpers import position_to_coordinates
import random
from backend.rl.single_tic import SingleTic


# Monte Carlo Method for Tic-Tac-Toe
class MonteCarlo:
    def __init__(self):
        self.game = SingleTic()
        self.values = {}
        self.policy = {}
        self.episode_history = []
        self.episode_count = 0



