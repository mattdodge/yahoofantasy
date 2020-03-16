from yahoofantasy import Context

c = Context()

leagues = c.get_leagues('mlb', 2019)
for league in leagues:
    print(league.name + " -- " + league.league_type)
