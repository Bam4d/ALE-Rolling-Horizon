import numpy as np
from ale_python_interface import ALEInterface

from environment import Environment


class ALEEnvironment(Environment):
    """
    A environment wrapper for the ALE environment
    """

    def __init__(self, rom_name, visible=True):
        super().__init__('Arcade Learning Environment')

        frame_skip = 20

        self._ale = ALEInterface()
        self._ale_sampler = ALEInterface()

        self._ale.setBool(b'display_screen', visible)
        #self._ale.setInt(b'frame_skip', frame_skip)

        #self._ale_sampler.setBool(b'display_screen', True)
        #self._ale_sampler.setInt(b'frame_skip', frame_skip)

        self._ale.loadROM(rom_name.encode('ascii'))
        self._ale_sampler.loadROM(rom_name.encode('ascii'))
        self._action_space = self._ale.getLegalActionSet()
        self._current_score = 0

    def evaluate_rollout(self, solution, discount_factor=0):
        #temp_state = self._ale.cloneState()

        temp_ale = self._ale.encodeState(self._ale.cloneState())
        temp_state = self._ale_sampler.decodeState(temp_ale)
        self._ale_sampler.restoreState(temp_state)

        prev_lives = self._ale.lives()
        total_rollout_reward = 0
        discount = 1
        for action in solution:
            rollout_reward = self._ale_sampler.act(action)

            if discount_factor is not None:
                rollout_reward *= discount
                discount *= discount_factor

            total_rollout_reward += rollout_reward

            if self._ale_sampler.game_over():
                break

        score_delta = total_rollout_reward + (self._ale_sampler.lives() - prev_lives)

        #self._ale.restoreState(temp_state)

        return score_delta

    def perform_action(self, action):
        reward = self._ale.act(action)
        self._current_score += reward

    def get_current_score(self):
        return self._current_score

    def get_current_lives(self):
        return self._ale.lives()

    def get_random_action(self):
        return np.random.choice(self._action_space)

    def is_game_over(self):
        return self._ale.game_over()
