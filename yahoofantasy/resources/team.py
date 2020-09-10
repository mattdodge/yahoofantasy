from yahoofantasy.util.logger import logger
from yahoofantasy.api.parse import as_list, from_response_object
from yahoofantasy.util.persistence import DEFAULT_TTL
from .player import Player


class Team():

    def __init__(self, ctx, league, team_id):
        self.ctx = ctx
        self.league = league
        self.id = team_id

    @property
    def manager(self):
        """ We can have multiple managers, so here's a shortcut to get 1 manager """
        return as_list(self.managers.manager)[0]

    def players(self, persist_ttl=DEFAULT_TTL):
        logger.debug("Looking up current players on team")
        data = self.ctx._load_or_fetch(
            f"team.{self.id}.players",
            f"team/{self.id}/players",
        )
        players = []
        for p in data['fantasy_content']['team']['players']['player']:
            player = Player()
            player = from_response_object(player, p)
            players.append(player)
        return players
