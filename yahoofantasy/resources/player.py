from yahoofantasy.api.parse import from_response_object, get_value
from yahoofantasy.stats.stat import Stat


class Player():

    def __init__(self, league):
        self.league = league
        # A cache of stats - a map of week num to the stats results
        self._stats_cache = {}

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
        data = self._fetch_stats(week_num)
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

    def get_points(self, week_num=None):
        """ Get this player's points for a given week or the whole season """
        data = self._fetch_stats(week_num)
        return get_value(data['fantasy_content']['league']['players']['player']['player_points']['total'])

    def _fetch_stats(self, week_num=None):
        """ Fetch the stats endpoint for a given week """
        if week_num in self._stats_cache:
            return self._stats_cache[week_num]
        keys = ('season', '')
        if week_num > 0:
            keys = (str(week_num), f"type=week;week={week_num}")
        data = self.league.ctx._load_or_fetch(
            f"player.{self.player_id}.stats.{self.league.id}.{keys[0]}",
            f"league/{self.league.id}/players;player_keys={self.player_key}/stats;{keys[1]}",
        )
        self._stats_cache[week_num] = data
        return data
