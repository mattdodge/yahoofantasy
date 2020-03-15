import os
from yahoofantasy import Context

YAHOO_CLIENT_ID = os.environ.get('YAHOO_CLIENT_ID')
YAHOO_CLIENT_SECRET = os.environ.get('YAHOO_CLIENT_SECRET')
YAHOO_REFRESH_TOKEN = os.environ.get('YAHOO_REFRESH_TOKEN')

c = Context(YAHOO_CLIENT_ID, YAHOO_CLIENT_SECRET, YAHOO_REFRESH_TOKEN)

leagues = c.get_leagues('mlb', 2019)
for league in leagues:
    print(league.name + " -- " + league.league_type)
