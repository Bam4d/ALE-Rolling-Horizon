
class Environment():

    def __init__(self, name):
        self._name = name

    def evaluate_rollout(self, solution, discount_factor=0):
        raise NotImplementedError

    def get_random_action(self):
        raise NotImplementedError

    def is_game_over(self):
        raise NotImplementedError

    def get_current_lives(self):
        raise NotImplementedError