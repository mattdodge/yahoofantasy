from collections import OrderedDict
from yahoo_sdk import logger
from yahoo_sdk.util.api import APIAttr


def get_value(val):
    """ Get the value to set based on a value from an XML response """

    # If it's a list we need one for each
    if isinstance(val, list):
        return [get_value(sub_val) for sub_val in val]

    if not isinstance(val, OrderedDict):
        logger.warn('Getting value of non OrderedDict...weird?')
        import pdb; pdb.set_trace()  # XXX BREAKPOINT
        return val

    if '$' in val:
        if len(val) > 1:
            logger.warn('Value has a $ but other stuff too')
        return val['$']

    return from_response_object(APIAttr(), val)


def from_response_object(obj, resp):
    """ Sets the attributes on obj based on resp """
    if not isinstance(resp, OrderedDict):
        raise RuntimeError(
            "Cannot parse response object that isn't OrderedDict")

    for attr in resp:
        setattr(obj, attr, get_value(resp[attr]))

    return obj
