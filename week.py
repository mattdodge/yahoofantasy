from yahoo_sdk.matchup import Matchup
from yahoo_sdk.api.parse import from_response_object


class Week():

    def __init__(self):
        self._matchups = list()

    @staticmethod
    def from_response(resp):
        week = Week()

        # If no matchup has been scheduled yet (i.e., playoffs) we ignore
        if 'matchup' not in resp:
            return week

        for matchup in resp['matchup']:
            matchup_obj = Matchup()
            week._matchups.append(from_response_object(
                matchup_obj, matchup))
        return week
