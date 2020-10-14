from yahoofantasy.api.parse import from_response_object, get_value
from yahoofantasy.stats.stat import Stat


class Player():

    def __init__(self, league):
        self.league = league

    @staticmethod
    def from_response(resp, league):
        return from_response_object(Player(league), resp)

    def __repr__(self):
        try:
            return f"Player: {self.name.full} ({self.display_position} - {self.editorial_team_abbr})"
        except AttributeError:
            return "Player: Unknown Player"

    def get_stats(self, week_num=None):
        """ Get this player's stats for a given week or the whole season """
        # First item is the peristence key, second is the API filter
        keys = ('season', '')
        if week_num > 0:
            keys = (str(week_num), f"type=week;week={week_num}")
        data = self.league.ctx._load_or_fetch(
            f"player.{self.player_id}.stats.{keys[0]}",
            f"league/{self.league.id}/players;player_keys={self.player_key}/stats;{keys[1]}",
        )
        stats_data = data['fantasy_content']['league']['players']['player']['player_stats']
        return [
            Stat.from_value(s, self.league.game_code)
            for s in get_value(stats_data).stats.stat
        ]

    def get_stat(self, stat_display, week_num=None):
        """ Get an individual player stat for a given week or the whole season """
        stats = [s for s in self.get_stats(week_num) if s.display == stat_display]
        if stats:
            return stats[0].value
        else:
            return None
