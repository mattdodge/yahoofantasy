from .mlb import stats as stats_mlb

league_types = {
    'mlb': stats_mlb,
}


def get_stat_and_value(stat_obj, league_type='mlb'):
    """ Given a stat_obj, get a tuple of stat name and stat value """
    global league_types
    stats = league_types.get(league_type)
    if not stats:
        raise ValueError("League type of {} isn't valid".format(league_type))

    stat_id = str(stat_obj.stat_id)
    stat_lookup = stats.get(stat_id)
    if not stat_lookup:
        raise ValueError("Stat ID {} not found in {} stats".format(stat_id, league_type))

    return stat_lookup['display'], stat_obj.value
