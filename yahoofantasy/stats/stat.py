from .utils import get_stat_from_value


class Stat:
    def __init__(self, id, name=None, display=None, order=None, value=None):
        self.id = id
        self.name = name
        self.display = display
        self.order = order
        self.value = value

    @staticmethod
    def from_dict(id, d):
        """Create a Stat object from an API stat dict"""
        return Stat(id=id, **d)

    @staticmethod
    def from_value(d, game="mlb"):
        """Create a Stat object from an API stat value"""
        # TODO: Get the game from a context or something like that
        return get_stat_from_value(d, game)

    def __repr__(self):
        return f"Stat {self.display} - {self.value}"
