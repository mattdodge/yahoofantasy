from yahoofantasy import logger
from os.path import isfile
import pickle
from time import time


def get_persistence_filename(persist_key):
    return "{}.yahoo.data".format(persist_key)


def save_league_to_persistence(league, persist_key):
    with open(get_persistence_filename(persist_key), 'wb') as fp:
        obj_to_save = {
            "time": int(time())
        }

        # Save whatever we can
        try:
            obj_to_save["league"] = league._raw
        except AttributeError:
            pass

        try:
            obj_to_save["teams"] = league._teams_raw
        except AttributeError:
            pass

        try:
            obj_to_save["players"] = league._players_raw
        except AttributeError:
            pass

        try:
            obj_to_save["standings"] = league.standings._raw
        except AttributeError:
            pass

        try:
            obj_to_save["weeks"] = {
                week_num + 1: league.weeks[week_num]._raw
                for week_num in range(len(league.weeks))}
        except AttributeError:
            pass

        pickle.dump(obj_to_save, fp)


def fetch_league_from_persistence(persist_key, ttl=1800):
    if not persist_key:
        return None

    filename = get_persistence_filename(persist_key)

    if not isfile(filename):
        logger.info("Persistence file not found")
        return None

    with open(get_persistence_filename(persist_key), 'rb') as fp:
        try:
            persisted_data = pickle.load(fp)
        except Exception:
            logger.exception("Could not load persistence data")
            return None

    # If we have persisted data and it's within the TTL, return it
    if not persisted_data:
        logger.warning("No persistence data found in file")
        return None

    if persisted_data.get('time') + ttl < time():
        logger.info("Persistence data expired, ignoring")
        return None

    return persisted_data
