from collections import defaultdict

games = defaultdict(dict)
games['mlb']['2001'] = 12
games['mlb']['2002'] = 12
games['mlb']['2003'] = 12
games['mlb']['2004'] = 12
games['mlb']['2005'] = 12
games['mlb']['2006'] = 12
games['mlb']['2007'] = 12
games['mlb']['2008'] = 12
games['mlb']['2009'] = 12
games['mlb']['2010'] = 12
games['mlb']['2011'] = 12
games['mlb']['2012'] = 12
games['mlb']['2013'] = 12
games['mlb']['2014'] = 12
games['mlb']['2015'] = 12
games['mlb']['2016'] = 12
games['mlb']['2017'] = 12
games['mlb']['2018'] = 12
games['mlb']['2019'] = 388
games['mlb']['2020'] = 398
# TODO: Fill in years prior to 2019


def get_game_id(game, season):
    season = str(season)
    if game not in games:
        raise ValueError("{} is not a valid game, must be 'mlb'".format(game))
    if season not in games[game]:
        raise ValueError(
            "{} is not a valid season for {}".format(season, game))
    return games[game][season]
