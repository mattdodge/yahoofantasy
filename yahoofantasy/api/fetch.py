from yahoofantasy.util.logger import logger
import requests

YURL = "https://fantasysports.yahooapis.com/fantasy/v2"


def make_request(url, token, league=False, **kwargs):
    if league:
        url = "league/{}/{}".format(league, url)
    logger.debug("Making request to {}".format(url))
    resp = requests.get(
        "{}/{}".format(YURL, url),
        headers={
            "Authorization": "Bearer {}".format(token),
            "User-Agent": "Mozilla/5.0",
        },
    )

    try:
        resp.raise_for_status()
    except Exception:
        logger.exception(
            "Bad response status ({}) for request".format(resp.status_code)
        )
        raise
    return resp.text
