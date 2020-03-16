

class League():

    def __init__(self):
        self.teams = list()
        self.players = list()
        self.standings = None
        self.weeks = list()

    def get_team(self, team_key):
        return next((t for t in self.teams if t.team_key == team_key), None)

    def __repr__(self):
        return "League: {}".format(getattr(self, 'name', 'Unnamed League'))
