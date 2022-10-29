from pydash import get
import requests
from time import time
from .resources.league import League
from yahoofantasy.util.logger import logger
from yahoofantasy.api.fetch import make_request
from yahoofantasy.api.parse import (
    parse_response,
    get_value,
    as_list,
    from_response_object,
)
from yahoofantasy.api.games import get_game_id
from yahoofantasy.util.persistence import DEFAULT_TTL, load, save

YAHOO_OAUTH_URL = "https://api.login.yahoo.com/oauth2"


class Context:
    def __init__(
        self, persist_key="", client_id=None, client_secret=None, refresh_token=None
    ):
        super().__init__()
        self._persist_key = persist_key
        auth_data = self._load("auth", default={}, ttl=-1)
        self._client_id = client_id or auth_data.get("client_id")
        self._client_secret = client_secret or auth_data.get("client_secret")
        self._refresh_token = refresh_token or auth_data.get("refresh_token")
        if not self._client_id or not self._client_secret or not self._refresh_token:
            raise ValueError(
                "Client ID, secret, and refresh token are required. "
                "Did you run 'yahoofantasy login' already?"
            )
        self._access_token = auth_data.get("access_token", None)
        self._access_token_expires = auth_data.get("access_token_expires", 0)

    def _get_access_token(self):
        logger.info("Fetching access token using refresh token")
        resp = requests.post(
            YAHOO_OAUTH_URL + "/get_token",
            data={
                "client_id": self._client_id,
                "client_secret": self._client_secret,
                "refresh_token": self._refresh_token,
                "grant_type": "refresh_token",
            },
        )
        if resp.status_code != 200:
            logger.error(
                "Error fetching access token - try "
                "running 'yahoofantasy login' again"
            )
            try:
                logger.error("ERROR: " + resp.json().get("error"))
                logger.error("DESCRIPTION: " + resp.json().get("error_description"))
            except Exception:
                pass
            resp.raise_for_status()
        body = resp.json()
        self._access_token = body.get("access_token")
        self._access_token_expires = time() + body.get("expires_in")
        self._refresh_token = body.get("refresh_token")

    def _load(self, persist_path, default, ttl=DEFAULT_TTL):
        """A shortcut to load data from persistence for this context"""
        return load(persist_path, default, ttl=ttl, persist_key=self._persist_key)

    def _save(self, persist_path, persist_val):
        """A shortcut to save data to persistence for this context"""
        return save(persist_path, persist_val, persist_key=self._persist_key)

    def _load_or_fetch(
        self, persist_path, *args, return_parsed=True, persist_ttl=DEFAULT_TTL, **kwargs
    ):
        """A shortcut to try loading from persistence but fetching if we miss

        Args:
            persist_path (str): A path to look for in persistence
            return_parsed (bool): Whether to return the parsed XML. Raw data is persisted
            *args/**kwargs: Arguments to pass to make_request if we need to
        """
        value = self._load(persist_path, default=None, ttl=persist_ttl)
        persistence_miss = value is None
        if persistence_miss:
            logger.debug(
                "Missed on persitence for {}, " "fetching from API".format(persist_path)
            )
            value = self.make_request(*args, **kwargs)
        else:
            logger.debug("Using persisted value for {}".format(persist_path))
        try:
            out = parse_response(value) if return_parsed else value
        except Exception:
            logger.warn("Error parsing XML response")
            logger.warn(f"Response body: {value}")
            raise
        # Save here so we make sure it was parseable - prevents saving error data
        if persistence_miss:
            self._save(persist_path, value)
        return out

    def make_request(self, url, *args, **kwargs):
        if not self._access_token or time() > self._access_token_expires:
            self._get_access_token()
        return make_request(url, *args, token=self._access_token, **kwargs)

    def get_leagues(self, game, season, persist_ttl=DEFAULT_TTL):
        """Get a list of all leagues for a given game and season

        Args:
            game (str) - the fantasy game we're looking at
            season (int/str) - the fantasy season to get leagues for
        """
        game_id = get_game_id(game, season)
        data = self._load_or_fetch(
            "leagues." + str(game_id),
            "users;use_login=1/games;game_keys={}/leagues".format(game_id),
            persist_ttl=persist_ttl,
        )
        leagues = []
        for league_data in as_list(
            get(data, "fantasy_content.users.user.games.game.leagues.league")
        ):
            league = League(self, get_value(league_data["league_key"]))
            from_response_object(league, league_data)
            leagues.append(league)
        return leagues
