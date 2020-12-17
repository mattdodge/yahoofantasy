from .player import Player
from yahoofantasy.api.parse import get_value, from_response_object


class Roster():

    def __init__(self, team, week_num=None):
        self.team = team
        self.week_num = week_num

    @property
    def players(self):
        return [
            Player.from_response(p.__dict__, self.team.league)
            for p in get_value(self._raw['players']).player
        ]

    @property
    def active_players(self):
        return [
            player for player in self.players
            if player.selected_position.position not in ('BN', 'IR')
        ]

    # TODO: Pre-fetch stats for all players on this roster
    def fetch_player_stats(self):
        pass
