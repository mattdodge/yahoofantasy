from collections import defaultdict

# Get these from this URL
# https://fantasysports.yahooapis.com/fantasy/v2/games;game_codes=mlb;seasons=2001,2002
games = defaultdict(dict)
games["mlb"]["2001"] = 12
games["mlb"]["2002"] = 39
games["mlb"]["2003"] = 74
games["mlb"]["2004"] = 98
games["mlb"]["2005"] = 113
games["mlb"]["2006"] = 147
games["mlb"]["2007"] = 171
games["mlb"]["2008"] = 195
games["mlb"]["2009"] = 215
games["mlb"]["2010"] = 238
games["mlb"]["2011"] = 253
games["mlb"]["2012"] = 268
games["mlb"]["2013"] = 308
games["mlb"]["2014"] = 328
games["mlb"]["2015"] = 346
games["mlb"]["2016"] = 357
games["mlb"]["2017"] = 370
games["mlb"]["2018"] = 378
games["mlb"]["2019"] = 388
games["mlb"]["2020"] = 398
games["mlb"]["2021"] = 404
games["mlb"]["2022"] = 412
games["mlb"]["2023"] = 422
games["mlb"]["2024"] = 431

games["nfl"]["2001"] = 57
games["nfl"]["2002"] = 49
games["nfl"]["2003"] = 79
games["nfl"]["2004"] = 101
games["nfl"]["2005"] = 124
games["nfl"]["2006"] = 153
games["nfl"]["2007"] = 175
games["nfl"]["2008"] = 199
games["nfl"]["2009"] = 222
games["nfl"]["2010"] = 242
games["nfl"]["2011"] = 257
games["nfl"]["2012"] = 273
games["nfl"]["2013"] = 314
games["nfl"]["2014"] = 331
games["nfl"]["2015"] = 348
games["nfl"]["2016"] = 359
games["nfl"]["2017"] = 371
games["nfl"]["2018"] = 380
games["nfl"]["2019"] = 390
games["nfl"]["2020"] = 399
games["nfl"]["2021"] = 406
games["nfl"]["2022"] = 414
games["nfl"]["2023"] = 423
games["nfl"]["2024"] = 449

games["nba"]["2001"] = 16
games["nba"]["2002"] = 67
games["nba"]["2003"] = 95
games["nba"]["2004"] = 112
games["nba"]["2005"] = 131
games["nba"]["2006"] = 165
games["nba"]["2007"] = 187
games["nba"]["2008"] = 211
games["nba"]["2009"] = 234
games["nba"]["2010"] = 249
games["nba"]["2011"] = 265
games["nba"]["2012"] = 304
games["nba"]["2013"] = 322
games["nba"]["2014"] = 342
games["nba"]["2015"] = 353
games["nba"]["2016"] = 364
games["nba"]["2017"] = 375
games["nba"]["2018"] = 385
games["nba"]["2019"] = 395
games["nba"]["2020"] = 402
games["nba"]["2021"] = 410
games["nba"]["2022"] = 418
games["nba"]["2023"] = 428

games["nhl"]["2001"] = 15
games["nhl"]["2002"] = 64
games["nhl"]["2003"] = 94
games["nhl"]["2004"] = 111
games["nhl"]["2005"] = 130
games["nhl"]["2006"] = 164
games["nhl"]["2007"] = 186
games["nhl"]["2008"] = 210
games["nhl"]["2009"] = 233
games["nhl"]["2010"] = 248
games["nhl"]["2011"] = 263
games["nhl"]["2012"] = 303
games["nhl"]["2013"] = 321
games["nhl"]["2014"] = 341
games["nhl"]["2015"] = 352
games["nhl"]["2016"] = 363
games["nhl"]["2017"] = 376
games["nhl"]["2018"] = 386
games["nhl"]["2019"] = 396
games["nhl"]["2020"] = 403
games["nhl"]["2021"] = 411
games["nhl"]["2022"] = 419
games["nhl"]["2023"] = 427


def get_game_id(game, season):
    season = str(season)
    if game not in games:
        raise ValueError(
            "{} is not a valid game, must be 'mlb', 'nba', 'nhl' or 'nfl'".format(game)
        )
    if season not in games[game]:
        raise ValueError("{} is not a valid season for {}".format(season, game))
    return games[game][season]


def _find_game_id(game, season, context):
    """Pass a valid yahoofantasy context and return the game ID

    This is a useful function for debuging or discovering a new game ID
    """
    from yahoofantasy.api.parse import parse_response
    from pydash import get

    resp = context.make_request(f"games;game_codes={game};seasons={season}")
    return get(parse_response(resp), "fantasy_content.games.game.game_key.$")
