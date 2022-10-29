import json
from os.path import join, dirname
from yahoofantasy.api.fetch import make_request
from yahoofantasy.api.parse import parse_response


def generate_stats(game, token):
    """Generate a python file with a stat mapping

    Args:
        game (string): The game to generate for (e.g. nfl, mlb)
        token: An access token to talk to the API

    Returns:
        None - writes a file called mlb.py with a stats export
    """
    stats_resp = parse_response(
        make_request("game/{}/stat_categories".format(game), token=token)
    )
    stats = stats_resp["fantasy_content"]["game"]["stat_categories"]["stats"][
        "stat"
    ]  # noqa E501
    mapping = {}
    for stat in stats:
        mapping[stat["stat_id"]["$"]] = {
            "name": stat["name"]["$"],
            "display": stat["display_name"]["$"],
            "order": int(stat["sort_order"]["$"]),
        }
    with open(join(dirname(__file__), "{}.py".format(game)), "w+") as f:
        f.write("stats=")
        json.dump(mapping, f)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("game")
    parser.add_argument("token")
    args = parser.parse_args()
    generate_stats(args.game, args.token)
