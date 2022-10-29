import inspect
import re
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
from yahoofantasy.util.logger import logger
from yahoofantasy.api.attr import APIAttr


def parse_response(resp):
    """Parse the raw XML response into OrderedDicts"""
    # Remove the namespace from the first XML element
    # Yahoo adds this namespace and the xml to json library
    # prefixes it on every json record, which is very annoying
    non_ns_text = re.sub(r"<fantasy_content[^>]*>", "<fantasy_content>", resp)

    # Return a JSON representation of the XML data returned from Yahoo
    return bf.data(fromstring(non_ns_text))


def get_value(val):
    """Get the value to set based on a value from an XML response"""

    # If it's a list we need one for each
    if isinstance(val, list):
        return [get_value(sub_val) for sub_val in val]

    if not isinstance(val, dict):
        return val

    if "$" in val:
        if len(val) > 1:
            logger.warn("Value has a $ but other stuff too")
        return val["$"]

    return from_response_object(APIAttr(), val)


def as_list(val):
    if isinstance(val, list):
        return val
    return [val]


def from_response_object(obj, resp, set_raw=False):
    """Sets the attributes on obj based on resp"""
    if not isinstance(resp, dict):
        raise RuntimeError("Cannot parse response object that isn't dict")

    # Set the raw data in case we want it on the object
    if set_raw:
        setattr(obj, "_raw", resp)

    ignore = [
        t[0]
        for t in sum(
            [
                inspect.getmembers(obj.__class__, predicate=inspect.ismethod),
                inspect.getmembers(obj.__class__, predicate=inspect.isfunction),
                inspect.getmembers(obj.__class__, predicate=inspect.isdatadescriptor),
            ],
            [],
        )
    ]
    for attr in resp:
        if attr in ignore:
            # Don't set any skipped/ignored attributes
            continue
        setattr(obj, attr, get_value(resp[attr]))

    return obj
