from yahoofantasy.api.parse import from_response_object, get_value
from yahoofantasy.util.persistence import DEFAULT_TTL
from yahoofantasy.util.logger import logger
from yahoofantasy.team import Team
from yahoofantasy.standings import Standings


class League():

    def __init__(self, ctx, league_id):
        self.ctx = ctx
        self.id = league_id
        self.players = list()
        self.weeks = list()

    def get_team(self, team_key):
        return next((t for t in self.teams if t.team_key == team_key), None)

    def teams(self, persist_ttl=DEFAULT_TTL):
        logger.debug("Looking up teams")
        data = self.ctx._load_or_fetch('teams.' + self.id, 'teams', league=self.id)
        teams = []
        for team in data['fantasy_content']['league']['teams']['team']:
            t = Team(self.ctx, self, get_value(team['team_key']))
            from_response_object(t, team)
            teams.append(t)
        return teams

    def standings(self, persist_ttl=DEFAULT_TTL):
        logger.debug("Looking up standings")
        data = self.ctx._load_or_fetch(
            'standings.' + self.id, 'standings', league=self.id)
        standings = []
        for team in data['fantasy_content']['league']['standings']['teams']['team']:
            standing = Standings(self.ctx, self, get_value(team['team_key']))
            from_response_object(standing, team)
            standings.append(standing)
        return standings

    def __repr__(self):
        return "League: {}".format(getattr(self, 'name', 'Unnamed League'))
