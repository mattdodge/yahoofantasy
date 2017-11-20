def make_test_request(url, token, league=None):
    if url == '':
        return get_test_league_response()
    elif url == 'teams':
        return get_test_teams_response()
    elif url == 'standings':
        return get_test_standings_response()
    elif url.startswith('scoreboard'):
        return get_test_scoreboard_response()

    raise RuntimeError("Invalid Request Made")


def __wrap_response(obj):
    return {
        'fantasy_content': {
            'league': obj
        }
    }


def get_test_league_response():
    return __wrap_response({
        'start_week': 1,
        'end_week': 3,
    })


def __get_test_team(team_id):
    return {
        'name': 'Team {}'.format(team_id),
        'team_key': team_id,
    }


def get_test_teams_response():
    return __wrap_response({
        'teams': {
            'team': [
                __get_test_team(1),
                __get_test_team(2),
                __get_test_team(3),
                __get_test_team(4),
            ]
        }
    })


def get_test_standings_response():
    return __wrap_response({
        'standings': {
            'teams': {
                'team': [
                    __get_test_team(1),
                    __get_test_team(2),
                    __get_test_team(3),
                    __get_test_team(4),
                ]
            }
        }
    })


def get_test_scoreboard_response():
    return __wrap_response({
        'scoreboard': {
            'matchups': {
                'matchup': [
                    {'teams': {
                        'team': [
                            __get_test_team(1),
                            __get_test_team(2),
                        ]
                    }},
                    {'teams': {
                        'team': [
                            __get_test_team(3),
                            __get_test_team(4),
                        ]
                    }},
                ]
            }
        }
    })
