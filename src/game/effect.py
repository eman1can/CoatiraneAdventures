from game.skill import ALL_FOES
from game.status_effect import HEALTH


class Effect:
    def __init__(self, target_type=ALL_FOES, type=HEALTH, duration=-1, st=None):
        self.target_type = target_type
        self.type = type
        self.duration = duration
        if st is None:
            st = []
        self.st = st

