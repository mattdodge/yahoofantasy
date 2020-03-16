from yahoofantasy.api.attr import APIAttr
from yahoofantasy.api.parse import from_response_object


class Standings():

    def __init__(self):
        self._standings = list()

    def update_team_references(self, league):
        """ Update each standings item with their league team reference """
        for standings_team in self._standings:
            setattr(standings_team,
                    '_team_obj',
                    league.get_team(standings_team.team_key))

    @staticmethod
    def from_response(resp):
        standings = Standings()
        for standing_result in resp:
            standings._standings.append(from_response_object(
                APIAttr(), standing_result))
        return standings
