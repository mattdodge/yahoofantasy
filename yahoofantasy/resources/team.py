from yahoofantasy.util.logger import logger
from yahoofantasy.api.parse import as_list, from_response_object
from yahoofantasy.util.persistence import DEFAULT_TTL
from .player import Player
from .roster import Roster


class Team:
    def __init__(self, ctx, league, team_id):
        self.ctx = ctx
        self.league = league
        self.id = team_id

    @property
    def manager(self):
        """We can have multiple managers, so here's a shortcut to get 1 manager"""
        return as_list(self.managers.manager)[0]

    def players(self, persist_ttl=DEFAULT_TTL):
        logger.debug("Looking up current players on team")
        data = self.ctx._load_or_fetch(
            f"team.{self.id}.players",
            f"team/{self.id}/players",
        )
        players = []
        for p in data["fantasy_content"]["team"]["players"]["player"]:
            player = Player(self.league)
            player = from_response_object(player, p)
            players.append(player)
        return players

    # TODO: Adjust this method to account for non-week based games
    def roster(self, week_num=None):
        """Fetch this team's roster for a given week

        If week_num is None fetch the live roster
        """
        # First item is the peristence key, second is the API filter
        keys = ("live", "")
        if week_num:
            keys = (str(week_num), f"week={week_num}")
        data = self.ctx._load_or_fetch(
            f"team.{self.id}.roster.{keys[0]}",
            f"team/{self.id}/roster;{keys[1]}",
        )
        roster_data = data["fantasy_content"]["team"]["roster"]
        roster = Roster(self, week_num)
        roster = from_response_object(roster, roster_data, set_raw=True)
        return roster

    def __repr__(self):
        return f"Team {self.name}"
