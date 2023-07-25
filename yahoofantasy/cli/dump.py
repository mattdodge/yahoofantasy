import click
from csv import DictWriter
from datetime import datetime
import pydash as _
import sys
from time import sleep
from yahoofantasy import Context, Team
from yahoofantasy.api.games import games
from .utils import warn, error

import logging

logging.basicConfig(level=logging.INFO)


@click.group()
@click.option("-o", "--output", default="stdout")
@click.option("-g", "--game", prompt=True, type=click.Choice(games.keys()))
@click.option("-s", "--season", prompt=True, default=datetime.now().year)
@click.pass_context
def dump(ctx, output, game, season):
    ctx.ensure_object(dict)
    ctx.obj["output"] = output
    yf_context = Context()
    leagues = yf_context.get_leagues(game, season)
    if len(leagues) == 1:
        league = leagues[0]
    else:
        click.echo("Your leagues:")
        for idx, league in enumerate(leagues):
            click.echo(f" {idx + 1}) {league.name}")
        league_num = click.prompt("Which league to use?")
        try:
            league = leagues[int(league_num) - 1]
        except Exception:
            error(f"{league_num} is an invalid selection", exit=True)
    ctx.obj["league"] = league


STAT_KEYS = set()


def _player_out(week_num, player, team, att_num=1):
    try:
        o = {
            "name": player.name.full,
            "week": week_num,
            "manager": team.manager.nickname,
            "team_id": team.id,
            "position": player.primary_position,
            "roster_position": player.selected_position.position,
            "points": player.get_points(week_num),
        }
        for stat in player.get_stats(week_num):
            STAT_KEYS.add(stat.display)
            o[stat.display] = stat.value
        return o
    except Exception as e:
        if att_num > 5:
            error("Failed 5 times, giving up. Returning limited data")
            return {
                "name": player.name.full,
                "week": week_num,
                "manager": team.manager.nickname,
                "team_id": team.id,
                "position": player.primary_position,
                "roster_position": player.selected_position.position,
                "points": "N/A",
            }
        warn(
            f"Failed to fetch week {week_num} stats for {player.name.full} ({player.player_key}), trying again in 2 minutes"
        )
        warn("   " + str(e))
        sleep(120)
        return _player_out(week_num, player, team, att_num + 1)


def _get_results(team, week_num):
    try:
        roster = team.roster(week_num)
        roster.fetch_player_stats()  # pre-fetch some stats to save time
    except Exception:
        error(
            "Failed to fetch player stats, this might be due to rate limiting. Trying again in 2 minutes"
        )
        sleep(120)
        return _get_results(team, week_num)
    results = []
    for player in roster.players:
        results.append(_player_out(week_num, player, team))
    return results


def _write_out(ctx, fieldnames, data):
    if ctx.obj["output"] == "stdout":
        of = sys.stdout
    else:
        of = open(ctx.obj["output"], "w+")
    writer = DictWriter(of, fieldnames=fieldnames)
    writer.writeheader()
    for res in data:
        writer.writerow(res)


@dump.command()
@click.pass_context
def performances(ctx):
    league = ctx.obj["league"]
    results = []

    with click.progressbar(
        length=(league.current_week - 1) * league.num_teams,
        label="Fetching performances",
    ) as bar:
        for week in league.weeks():
            if (
                week.week_num > league.current_week
                or week.matchups[0].status != "postevent"
            ):
                bar.update(league.num_teams)
                continue
            for matchup in week.matchups:
                results.extend(_get_results(matchup.team1, week.week_num))
                bar.update(1)
                results.extend(_get_results(matchup.team2, week.week_num))
                bar.update(1)
    fieldnames = [
        "name",
        "week",
        "manager",
        "team_id",
        "position",
        "roster_position",
        "points",
    ] + sorted(STAT_KEYS)
    _write_out(ctx, fieldnames, results)


@dump.command()
@click.pass_context
def matchups(ctx):
    league = ctx.obj["league"]
    results = []

    with click.progressbar(
        length=(league.current_week - 1) * league.num_teams, label="Fetching matchups"
    ) as bar:
        for week in league.weeks():
            if (
                week.week_num > league.current_week
                or week.matchups[0].status != "postevent"
            ):
                bar.update(league.num_teams)
                continue
            for matchup in week.matchups:
                team1_win = (
                    matchup.teams.team[0].team_points.total
                    > matchup.teams.team[1].team_points.total
                )
                results.append(
                    {
                        "week": week.week_num,
                        "win": team1_win,
                        "manager": matchup.team1.manager.nickname,
                        "points": matchup.teams.team[0].team_points.total,
                        "proj_points": matchup.teams.team[
                            0
                        ].team_projected_points.total,
                        "opponent": matchup.team2.manager.nickname,
                        "opp_points": matchup.teams.team[1].team_points.total,
                        "opp_proj_points": matchup.teams.team[
                            1
                        ].team_projected_points.total,
                    }
                )
                bar.update(1)
                results.append(
                    {
                        "week": week.week_num,
                        "win": not team1_win,
                        "manager": matchup.team2.manager.nickname,
                        "points": matchup.teams.team[1].team_points.total,
                        "proj_points": matchup.teams.team[
                            1
                        ].team_projected_points.total,
                        "opponent": matchup.team1.manager.nickname,
                        "opp_points": matchup.teams.team[0].team_points.total,
                        "opp_proj_points": matchup.teams.team[
                            0
                        ].team_projected_points.total,
                    }
                )
                bar.update(1)
    fieldnames = [
        "week",
        "manager",
        "win",
        "points",
        "proj_points",
        "opponent",
        "opp_points",
        "opp_proj_points",
    ]
    _write_out(ctx, fieldnames, results)


@dump.command()
@click.pass_context
def draftresults(ctx):
    league = ctx.obj["league"]
    draft_results = sorted(league.draft_results(), key=lambda dr: dr.pick)
    results = []
    for result in draft_results:
        results.append(
            {
                "pick": result.pick,
                "round": result.round,
                "manager": result.team.manager.nickname,
                "player": result.player.name.full,
                "pos": result.player.display_position,
            }
        )
    fieldnames = ["pick", "round", "manager", "player", "pos"]
    _write_out(ctx, fieldnames, results)


@dump.command()
@click.pass_context
def transactions(ctx):
    league = ctx.obj["league"]
    transactions = sorted(league.transactions(), key=lambda dr: dr.timestamp)
    results = []
    for trans in transactions:
        for player in trans.involved_players:
            from_team = player.from_team
            to_team = player.to_team
            ts = datetime.fromtimestamp(trans.timestamp)
            results.append(
                {
                    "type": trans.type,
                    "player_type": player.transaction_data.type,
                    "player": player.name.full,
                    "from": from_team.name
                    if isinstance(from_team, Team)
                    else from_team,
                    "to": to_team.name if isinstance(to_team, Team) else to_team,
                    "ts": ts.strftime("%m/%d/%Y, %H:%M:%S"),
                    "week_idx": ts.strftime("%W"),
                    "bid": _.get(trans, "faab_bid", ""),
                }
            )
    fieldnames = [
        "type",
        "player_type",
        "player",
        "from",
        "to",
        "ts",
        "week_idx",
        "bid",
    ]
    _write_out(ctx, fieldnames, results)
