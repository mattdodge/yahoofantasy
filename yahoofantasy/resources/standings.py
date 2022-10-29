class Standings:
    def __init__(self, ctx, league, team_id):
        self.ctx = ctx
        self.league = league
        self.id = team_id

        self._standings = list()

    @property
    def team(self):
        return self.league.get_team(self.id)
