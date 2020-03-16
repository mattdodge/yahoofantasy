from pydash import get
import requests
from time import time
from yahoofantasy.league import League
from yahoofantasy.util.logger import logger
from yahoofantasy.api.fetch import make_request
from yahoofantasy.api.parse import (
    parse_response,
    get_value,
    as_list,
    from_response_object,
)
from yahoofantasy.api.games import get_game_id
from yahoofantasy.util.persistence import load_obj_from_persistence, save_obj_to_persistence

YAHOO_OAUTH_URL = "https://api.login.yahoo.com/oauth2"


class Context():

    def __init__(self, persist_key='',
                 client_id=None, client_secret=None, refresh_token=None):
        super().__init__()
        self._persist_key = persist_key
        auth_data = load_obj_from_persistence('auth', default={}, persist_key=persist_key, ttl=-1)
        self._client_id = client_id or auth_data.get('client_id')
        self._client_secret = client_secret or auth_data.get('client_secret')
        self._refresh_token = refresh_token or auth_data.get('refresh_token')
        if not self._client_id or not self._client_secret or not self._refresh_token:
            raise ValueError("Client ID, secret, and refresh token are required. "
                             "Did you run 'yahoofantasy login' already?")
        self._access_token = auth_data.get('access_token', None)
        self._access_token_expires = auth_data.get('access_token_expires', 0)

    def _get_access_token(self):
        logger.info("Fetching access token using refresh token")
        resp = requests.post(YAHOO_OAUTH_URL + "/get_token", data={
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'refresh_token': self._refresh_token,
            'grant_type': 'refresh_token',
        })
        if resp.status_code != 200:
            logger.error("Error fetching access token - try "
                         "running 'yahoofantasy login' again")
            try:
                logger.error(
                    "ERROR: " + resp.json().get('error'))
                logger.error(
                    "DESCRIPTION: " + resp.json().get('error_description'))
            except Exception:
                pass
            resp.raise_for_status()
        body = resp.json()
        self._access_token = body.get('access_token')
        self._access_token_expires = time() + body.get('expires_in')
        self._refresh_token = body.get('refresh_token')

    def make_request(self, url, *args, **kwargs):
        if not self._access_token or time() > self._access_token_expires:
            self._get_access_token()
        return make_request(url, *args, token=self._access_token, **kwargs)

    def get_leagues(self, game, season, persistence_ttl=1800):
        """ Get a list of all leagues for a given game and season

        Args:
            game (str) - the fantasy game we're looking at, must be 'mlb' for now
            season (int/str) - the fantasy season to get leagues for
        """
        game_id = get_game_id(game, season)
        raw = load_obj_from_persistence(
            'leagues', default=None, ttl=persistence_ttl, persist_key=self._persist_key)
        if raw is None:
            raw = self.make_request(
                "users;use_login=1/games;game_keys={}/leagues".format(game_id))
            save_obj_to_persistence('leagues', raw, persist_key=self._persist_key)
        else:
            logger.debug("Loading raw league data from persistence")
        parsed = parse_response(raw)
        leagues = []
        for league_data in as_list(get(
                parsed, 'fantasy_content.users.user.games.game.leagues.league')):
            league = League(get_value(league_data['league_key']))
            from_response_object(league, league_data)
            leagues.append(league)
        return leagues
