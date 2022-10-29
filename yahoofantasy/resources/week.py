from pydash import get
from .matchup import Matchup
from yahoofantasy.api.parse import from_response_object


class Week:
    def __init__(self, ctx, league, week_num):
        self.ctx = ctx
        self.league = league
        self.week_num = week_num
        self.matchups = []

    def sync(self):
        week_data = self.ctx._load_or_fetch(
            "weeks.{}.{}".format(self.league.id, self.week_num),
            "scoreboard;week={}".format(self.week_num),
            league=self.league.id,
        )
        matchup_data = get(week_data, "fantasy_content.league.scoreboard.matchups")
        if "matchup" not in matchup_data:
            return
        self.matchups = []
        for matchup in matchup_data["matchup"]:
            matchup_obj = Matchup(self.ctx, self.league, self)
            self.matchups.append(from_response_object(matchup_obj, matchup))
