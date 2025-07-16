# Let different policies palay against each other
import numpy as np
from backend.helpers import position_to_coordinates
import random
from backend.rl.single_tic import SingleTic
from backend.rl.model_free.monte_carlo import MonteCarlo
from backend.rl.model_free.temporal_diff import TemporalDifference
from backend.rl.dynamic_programming.value_iter import ValueIteration
from backend.rl.dynamic_programming.policy_iter import PolicyIteration


NOTES = """
Temporal Difference and Monte Carlo are both model-free methods, and perform much worse than their model-based counterparts.

It is possible to beat the policies given by the model-based methods, since they are not perfect and have not explored every state.
"""

def monte_carlo_policy():
    mc = MonteCarlo()
    policy = mc.train()
    return policy

def temporal_diff_policy():
    td = TemporalDifference()
    policy = td.train_full()
    return policy

def value_iteration_policy():
    vi = ValueIteration()
    policy = vi.run_value_iteration()
    return policy

def policy_iteration_policy():
    pi = PolicyIteration()
    policy = pi.run_policy_iteration()
    return policy

def main():
    policy_1 = monte_carlo_policy()
    policy_2 = temporal_diff_policy()
    # policy_3 = value_iteration_policy()
    # policy_4 = policy_iteration_policy()

    SingleTic.simulate_ai_game(policy_1, policy_2)
    # SingleTic.simulate_ai_game(policy_1, policy_3)
    # SingleTic.simulate_ai_game(policy_1, policy_4)
    # SingleTic.simulate_ai_game(policy_2, policy_3)


if __name__ == "__main__":
    main()