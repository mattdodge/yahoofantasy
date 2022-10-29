from .player import Player
from yahoofantasy.api.parse import get_value, from_response_object
from yahoofantasy.util.logger import logger


class Roster:
    def __init__(self, team, week_num=None):
        self.team = team
        self.week_num = week_num
        # A cached list of player object references
        self._players = []

    @property
    def players(self):
        if self._players:
            return self._players
        self._players = [
            Player.from_response(p.__dict__, self.team.league)
            for p in get_value(self._raw["players"]).player
        ]
        return self._players

    @property
    def active_players(self):
        return [
            player
            for player in self.players
            if player.selected_position.position not in ("BN", "IR")
        ]

    def fetch_player_stats(self):
        """Fetch the stats for every player on the roster for the given week"""
        player_keys = ",".join([p.player_key for p in self.players])
        keys = ("season", "")
        if self.week_num:
            keys = (str(self.week_num), f"type=week;week={self.week_num}")
        data = self.team.league.ctx._load_or_fetch(
            f"roster.{self.team.id}.stats.{self.team.league.id}.{keys[0]}",
            f"league/{self.team.league.id}/players;player_keys={player_keys}/stats;{keys[1]}",
        )
        # Populate the stats caches of the individual players too
        player_map = {p.player_key: p for p in self.players}
        player_refs = data["fantasy_content"]["league"]["players"]["player"]
        for player_ref in player_refs:
            player_key = get_value(player_ref["player_key"])
            player_obj = player_map.get(player_key)
            if not player_obj:
                logger.warn(
                    f"Player stats found for {player_key} but they are not on the roster"
                )
                continue
            player_obj._stats_cache[self.week_num] = player_ref
        return data
