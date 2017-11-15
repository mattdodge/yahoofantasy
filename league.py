from yahoo_sdk.util.api import make_request
from yahoo_sdk.team import Team
from yahoo_sdk.standings import Standings


class League():

    def __init__(self, league_id):
        self.league_id = league_id

        self.teams = list()
        self.standings = None

    def fetch(self):
        """ Fetch all information about this league """
        self.__fetch_teams()
        self.__fetch_standings()

    def get_team(self, team_key):
        return next((t for t in self.teams if t.team_key == team_key), None)

    def __fetch_teams(self):
        results = make_request('teams', league=self.league_id)
        for team in results['fantasy_content']['league']['teams']['team']:
            t = Team.from_response(team)
            self.teams.append(t)

    def __fetch_standings(self):
        results = make_request('standings', league=self.league_id)
        self.standings = Standings.from_response(
            results['fantasy_content']['league']['standings']['teams']['team'])
        self.standings.update_team_references(self)

