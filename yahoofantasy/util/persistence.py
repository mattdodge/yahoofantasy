from copy import copy
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
    """Save a key/value pair to persistence

    Args:
        save_path: A pydash path to where the data should be saved
        save_val: The value/object to save, it will be pickled
        persist_key (str): A unique identifier for the persistence file
        overwrite (bool): If True, will wipe out existing persistence
    """
    filename = get_persistence_filename(persist_key)
    persisted_data = {}
    if not overwrite and isfile(filename):
        with open(filename, "rb") as fp:
            persisted_data = pickle.load(fp)
    # Save the time we stored this too, for TTL later
    persisted_data = set_(persisted_data, save_path + "__time", time())
    persisted_data = set_(persisted_data, save_path, save_val)
    with open(filename, "wb") as fp:
        pickle.dump(persisted_data, fp)
    set_(CURRENT_PERSISTENCE, save_path + "__time", time())
    set_(CURRENT_PERSISTENCE, save_path, save_val)


def load(load_path, default=_DEFAULT_SINGLETON, ttl=DEFAULT_TTL, persist_key=""):
    """Load an object from a key path in persistence

    Args:
        load_path (str): A pydash path to where the data is stored in persistence
        persist_key (str): A unique identifier for the persistence file
    """
    if CURRENT_PERSISTENCE:
        persisted_data = CURRENT_PERSISTENCE
    else:
        filename = get_persistence_filename(persist_key)
        if not isfile(filename):
            persisted_data = {}
        else:
            with open(filename, "rb") as fp:
                persisted_data = pickle.load(fp)
                CURRENT_PERSISTENCE.clear()
                CURRENT_PERSISTENCE.update(persisted_data)
    time_saved = get(persisted_data, load_path + "__time", 0)
    if ttl >= 0 and time_saved + ttl < time():
        logger.debug("Persistence data expired, ignoring")
        out = default
    else:
        out = get(persisted_data, load_path, default)
    if out is _DEFAULT_SINGLETON:
        raise ValueError("Path {} not found in persistence".format(load_path))
    return out


def clear(ignore_keys=[], persist_key=""):
    out = copy(CURRENT_PERSISTENCE)
    for key in list(CURRENT_PERSISTENCE.keys()):
        if key in ignore_keys or key.replace("__time", "") in ignore_keys:
            continue
        del out[key]
        # Also clear the in-memory persistence cache
        del CURRENT_PERSISTENCE[key]
    filename = get_persistence_filename(persist_key)
    with open(filename, "wb") as fp:
        pickle.dump(out, fp)
