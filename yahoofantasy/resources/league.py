from yahoofantasy.api.games import get_game_id
from yahoofantasy.api.parse import from_response_object, get_value
from yahoofantasy.util.persistence import DEFAULT_TTL
from yahoofantasy.util.logger import logger
from .team import Team
from .standings import Standings
from .week import Week
from .draft_result import DraftResult
from .transaction import Transaction
from .player import Player


class League:
    def __init__(self, ctx, league_id):
        self.ctx = ctx
        self.id = league_id

    def get_team(self, team_key):
        return next((t for t in self.teams() if t.team_key == team_key), None)

    def teams(self, persist_ttl=DEFAULT_TTL):
        logger.debug("Looking up teams")
        data = self.ctx._load_or_fetch("teams." + self.id, "teams", league=self.id)
        teams = []
        for team in data["fantasy_content"]["league"]["teams"]["team"]:
            t = Team(self.ctx, self, get_value(team["team_key"]))
            from_response_object(t, team)
            teams.append(t)
        return teams

    def players(self, persist_ttl=DEFAULT_TTL):
        logger.debug("Looking up players")
        START = 0
        COUNT = 25
        data = self.ctx._load_or_fetch(f"players.{self.id}.{START}", f"players;count={COUNT};start={START}", league=self.id)
        players = []
        while "player" in data["fantasy_content"]["league"]["players"]:
            for player in data["fantasy_content"]["league"]["players"]["player"]:
                p = Player(self)
                from_response_object(p, player)
                players.append(p)
            START += COUNT
            data = self.ctx._load_or_fetch(f"players.{self.id}.{START}", f"players;count={COUNT};start={START}", league=self.id)
        return players

    def standings(self, persist_ttl=DEFAULT_TTL):
        logger.debug("Looking up standings")
        data = self.ctx._load_or_fetch(
            "standings." + self.id, "standings", league=self.id
        )
        standings = []
        for team in data["fantasy_content"]["league"]["standings"]["teams"]["team"]:
            standing = Standings(self.ctx, self, get_value(team["team_key"]))
            from_response_object(standing, team)
            standings.append(standing)
        return standings

    def weeks(self, persist_ttl=DEFAULT_TTL):
        if not self.start_week or not self.end_week:
            raise AttributeError(
                "Can't fetch weeks for a league without start/end weeks. Is it a "
                "head-to-head league? Did you sync your league already?"
            )
        logger.debug("Looking up weeks")
        out = []
        for week_num in range(self.start_week, self.end_week + 1):
            week = Week(self.ctx, self, week_num)
            week.sync()
            out.append(week)
        return out

    def draft_results(self, persist_ttl=DEFAULT_TTL):
        results = []
        for team in self.teams(persist_ttl):
            data = self.ctx._load_or_fetch(
                "draftresults." + team.id, f"team/{team.id}/draftresults;out=players"
            )
            for result in data["fantasy_content"]["team"]["draft_results"][
                "draft_result"
            ]:
                dr = DraftResult(self, team)
                from_response_object(dr, result)
                results.append(dr)
        return results

    def transactions(self, persist_ttl=DEFAULT_TTL):
        results = []
        data = self.ctx._load_or_fetch(
            "transactions." + self.id, "transactions", league=self.id
        )
        for result in data["fantasy_content"]["league"]["transactions"]["transaction"]:
            trans = Transaction.from_response(result, self)
            results.append(trans)
        return results

    def __repr__(self):
        return "League: {}".format(getattr(self, "name", "Unnamed League"))

    @property
    def past_league_id(self):
        """Get this league's previous year's league ID and game code

        If the commissioner has configured this, return a tuple of
        (game_code, league_id) for the previous season for this league

        Returns None if the league is not configured for league history

        Example:
        >>> lg = ctx.get_leagues('mlb', 2022)[0]
        >>> lg.past_league_id
        (404, 12345)

        404 represents the MLB game code for 2021, 12345 is the league ID
        """
        full_league_key = getattr(self, "renew", None)
        if not full_league_key:
            return None
        full_league_key = str(full_league_key)
        # Full league keys are a combination of the game code and the league ID
        # In the raw response they look like 333_12345 where 333 is the game code and
        # 12345 is the league ID. However, due to how python ignores underscores in
        # numbers, specifically in the XML parsing library, it will come through as
        # a single integer that looks like 33312345
        # We can make an educated guess about what the league ID actually is though
        # given reasonable game codes based on our current league. We'll do that here
        current_season = self.season
        while True:
            try:
                last_years_game_code = get_game_id(self.game_code, current_season - 1)
            except ValueError:
                # We don't have any information about the previous year, give up
                return None
            last_years_game_code = str(last_years_game_code)
            if full_league_key.startswith(last_years_game_code):
                return (
                    int(last_years_game_code),
                    int(full_league_key[len(last_years_game_code) :]),
                )
            else:
                # Try the previous year
                current_season -= 1
