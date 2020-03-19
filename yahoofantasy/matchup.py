from yahoofantasy.api.parse import as_list


class Matchup():

    def __init__(self, ctx, league, week):
        self.ctx = ctx
        self.league = league
        self.week = week

    @property
    def team1(self):
        return self.league.get_team(as_list(self.teams.team)[0].team_key)

    @property
    def team2(self):
        return self.league.get_team(as_list(self.teams.team)[1].team_key)
