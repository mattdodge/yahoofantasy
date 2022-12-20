from .mlb import stats as stats_mlb
from .nfl import stats as stats_nfl
from .nba import stats as stats_nba
from .nhl import stats as stats_nhl

league_types = {
    "mlb": stats_mlb,
    "nfl": stats_nfl,
    "nba": stats_nba,
    "nhl": stats_nhl
}


def get_stat_from_value(stat_obj, league_type="mlb"):
    """Given a stat_obj, get a Stat object with an associated value"""
    global league_types
    stats = league_types.get(league_type)
    if not stats:
        raise ValueError("League type of {} isn't valid".format(league_type))

    stat_id = str(stat_obj.stat_id)
    stat_lookup = stats.get(stat_id)
    if not stat_lookup:
        raise ValueError(
            "Stat ID {} not found in {} stats".format(stat_id, league_type)
        )

    from .stat import Stat

    stat = Stat.from_dict(stat_id, stat_lookup)
    stat.value = stat_obj.value
    return stat


def get_stat_from_stat_list(stat_display, stat_list, order=None, league_type="mlb"):
    global league_types
    stats = league_types.get(league_type)
    if not stats:
        raise ValueError("League type of {} isn't valid".format(league_type))

    target_stat_id = None
    for stat_id, stat_data in stats.items():
        # Some stats are the same for hitters/pitchers, if we specify the order we'll
        # know which stat we're talking about
        # 1 means higher is better, so for Runs order=1 is for hitters, 0 for pitchers
        if stat_data["display"] == stat_display and (
            order is None or order == stat_data["order"]
        ):
            target_stat_id = stat_id
            break
    else:
        raise ValueError(
            "Stat {} not found in {} stats".format(stat_display, league_type)
        )

    for stat in stat_list:
        if str(stat.stat_id) == str(target_stat_id):
            return stat.value
    else:
        raise ValueError(
            "Stat {}(id:{}) not found in input stat list".format(stat_display, stat_id)
        )
