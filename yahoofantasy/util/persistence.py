from pydash import set_, get
from yahoofantasy.util.logger import logger
from os.path import isfile
import pickle
from time import time

_DEFAULT_SINGLETON = "__secret_default_function_argument"
DEFAULT_TTL = 3600  # 1.5 hours of persistence by default
# An in-memory cache of the current persistence
# This won't work if multiple threads are writing to the persitence file,
# but I think we're ok for now
CURRENT_PERSISTENCE = {}


def get_persistence_filename(persist_key):
    return "{}.yahoofantasy".format(persist_key)


def save(save_path, save_val, persist_key="", overwrite=False):
    """ Save a key/value pair to persistence

    Args:
        save_path: A pydash path to where the data should be saved
        save_val: The value/object to save, it will be pickled
        persist_key (str): A unique identifier for the persistence file
        overwrite (bool): If True, will wipe out existing persistence
    """
    global CURRENT_PERSISTENCE
    filename = get_persistence_filename(persist_key)
    persisted_data = {}
    if not overwrite and isfile(filename):
        with open(filename, 'rb') as fp:
            persisted_data = pickle.load(fp)
    # Save the time we stored this too, for TTL later
    persisted_data = set_(persisted_data, save_path + '__time', time())
    persisted_data = set_(persisted_data, save_path, save_val)
    with open(filename, 'wb') as fp:
        pickle.dump(persisted_data, fp)
    CURRENT_PERSISTENCE = set_(CURRENT_PERSISTENCE, save_path + '__time', time())
    CURRENT_PERSISTENCE = set_(CURRENT_PERSISTENCE, save_path, save_val)


def load(load_path, default=_DEFAULT_SINGLETON, ttl=DEFAULT_TTL, persist_key=""):
    """ Load an object from a key path in persistence

    Args:
        load_path (str): A pydash path to where the data is stored in persistence
        persist_key (str): A unique identifier for the persistence file
    """
    global CURRENT_PERSISTENCE
    if CURRENT_PERSISTENCE:
        persisted_data = CURRENT_PERSISTENCE
    else:
        filename = get_persistence_filename(persist_key)
        if not isfile(filename):
            persisted_data = {}
        else:
            with open(filename, 'rb') as fp:
                persisted_data = pickle.load(fp)
                CURRENT_PERSISTENCE = persisted_data
    time_saved = get(persisted_data, load_path + '__time', 0)
    if ttl >= 0 and time_saved + ttl < time():
        logger.info("Persistence data expired, ignoring")
        out = default
    else:
        out = get(persisted_data, load_path, default)
    if out is _DEFAULT_SINGLETON:
        raise ValueError("Path {} not found in persistence".format(load_path))
    return out


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


def fetch_league_from_persistence(persist_key, ttl=DEFAULT_TTL):
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
