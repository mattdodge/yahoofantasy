from yahoofantasy import logger
from yahoofantasy.api.fetch import make_request
from yahoofantasy.api.parse import from_response_object, parse_response
from yahoofantasy.util.persistence import fetch_league_from_persistence
from yahoofantasy.league import League
from yahoofantasy.team import Team
from yahoofantasy.player import Player
from yahoofantasy.week import Week
from yahoofantasy.standings import Standings


class Connection():

    def __init__(self, league_id, persist=None):
        self.__persist_key = persist
        self._league_id = league_id
        self.league = League()

    def fetch(self, persist_ttl=1800):
        """ Fetch all information about this league """
        persisted_raw = fetch_league_from_persistence(
            self.__persist_key, ttl=persist_ttl)

        if not persisted_raw:
            persisted_raw = {}

        league = League()

        self.__parse_league(league, raw=persisted_raw.get('league'))
        self.__parse_teams(league, raw=persisted_raw.get('teams'))
        self.__parse_players(league, raw=persisted_raw.get('players'))
        # self.__parse_standings(league, raw=persisted_raw.get('standings'))
        # self.__parse_weeks(league, raw=persisted_raw.get('weeks'))

        return league

    def __parse_league(self, league, raw=None):
        if raw is None:
            raw = make_request('', league=self._league_id)
        league._raw = raw
        parsed = parse_response(raw)
        from_response_object(league, parsed['fantasy_content']['league'])

    def __parse_teams(self, league, raw=None):
        if raw is None:
            raw = make_request('teams', league=self._league_id)
        league._teams_raw = raw
        parsed = parse_response(raw)
        for team in parsed['fantasy_content']['league']['teams']['team']:
            t = Team.from_response(team)
            league.teams.append(t)

    def __parse_players(self, league, raw=None):
        if raw is None:
            raw = make_request('players', league=self._league_id)
        league._players_raw = raw
        parsed = parse_response(raw)
        for player in parsed['fantasy_content']['league']['players']['player']:
            p = Player.from_response(player)
            league.players.append(p)

    def __parse_standings(self, league, raw=None):
        if raw is None:
            raw = make_request('standings', league=self._league_id)
        parsed = parse_response(raw)
        standings = Standings.from_response(
            parsed['fantasy_content']['league']['standings']['teams']['team'])
        standings._raw = raw
        league.standings = standings
        league.standings.update_team_references(league)

    def __parse_weeks(self, league, raw=None):
        for week_num in range(league.start_week, league.end_week + 1):
            if not raw or not raw.get(week_num):
                raw_week = make_request('scoreboard;week={}'.format(week_num),
                                        league=self._league_id)
            else:
                raw_week = raw.get(week_num)

            parsed = parse_response(raw_week)
            week = Week.from_response(
                parsed['fantasy_content']['league']['scoreboard']['matchups'])

            week._raw = raw_week
            league.weeks.append(week)
