# Yahoo Fantasy API Wrapper

The Yahoo Fantasy Sports API is difficult to comprehend, has [this strange one-page documentation setup](https://developer.yahoo.com/fantasysports/guide/) that is hard to navigate, and seems to only want to conform to a small portion of the OAuth spec. This library/SDK makes your life easier if you want to write an app that interfaces with the Yahoo Fantasy Sports API.

This library will work for any Yahoo Fantasy Sports API leagues/teams. It contains some common constructs and helper methods for head-to-head MLB leagues at this time. More sports and league types are planned for the future.

## Installation

```
pip install yahoofantasy
```

You will also need a application registered on the [Yahoo Developer Site](https://developer.yahoo.com/apps/). You'll need your client ID and secret. The app just needs to have read permissions. See below for instructions on how to set up your Yahoo Developer application if you don't have one already.

## Basic Usage

You're going to want to start off by logging in to your Yahoo Developer application, then creating a context. This context is where all of your API requests will originate and league information will live.

```bash
$ yahoofantasy login
```

Once you've logged in, create a context and use that to make requests. For example, to fetch all of your leagues for a given game/season:
```python
from yahoofantasy import Context

ctx = Context()
leagues = ctx.get_leagues('mlb', 2020)
for league in leagues:
    print(league.name + " -- " + league.league_type)
```

## Retreiving Access and Refresh Tokens

You can use the built-in `yahoofantasy` CLI to obtain an access token and refresh token for your application. Follow these steps:

1. Set up your Yahoo application to have a callback/redirect URI of `https://localhost:8000`. If you already have an app that points to your local host on a different port or different path that's ok, you can customize later on.
2. Install `yahoofantasy` if you haven't already
```bash
$ pip install yahoofantasy
```
3. Log in with your Yahoo account. This command will launch a browser that will ask you to authenticate to your app. It will then store the token in a local file that can be consumed by the yahoofantasy SDK.
```bash
$ yahoofantasy login
```

*NOTE*: If you see a browser certificate warning that is ok, proceed anyway past the warning to save your token. This warning happens because Yahoo requires an HTTPS redirect URI and the local server uses an untrusted certificate.

Try `yahoofantasy login --help` for some advanced options, like customizing the port or redirect URI

## Concepts

There is a general hierarchy that head-to-head leagues will follow. This hierarchy is represented with classes within this library. This code walkthrough will help you understand the organization of the library. The following examples are intended to be read sequentially and assume you have a **Context** with your logged in Yahoo credentials called `ctx`.

* Your account will belong to one or more **League** objects.
```python
for league in ctx.get_leagues('mlb', 2019):
    print(f"{league.id} - {league.name} ({league.league_type})")
```
    
* A **League** will contain multiple **Team** objects.
```python
from yahoofantasy import League

league = League(ctx, '388.l.25000')  # Use a manual league ID or get it from league.id above
for team in league.teams():
    print(f"Team Name: {team.name}\tManager: {team.manager.nickname}")
```

* A **Team** has multiple **Player** objects that define their lineup. This is their current lineup and not a lineup for a given week
```python
for team in league.standings():
		players = team.players()
		for player in players:
				print(f"Player: {player.name.full}")
```

* A **League** has **Standings**, which is an ordered list of **Team** objects.
```python
for team in league.standings():
    outcomes = team.team_standings.outcome_totals
    print(f"#{team.team_standings.rank}\t{team.name}\t"
          f"({outcomes.wins}-{outcomes.losses}-{outcomes.ties})")
```

* A **League** will contain multiple **Week** objects. A **Week** contains multiple **Matchup** objects, which are a head-to-head matchup of two **Team** objects for that week.
```python
week_3 = league.weeks()[2]
for matchup in week_3.matchups:
    print(f"{matchup.team1.name} vs {matchup.team2.name}")
```

* A **Matchup** will have multiple **Stat** objects for the two teams. A **Stat** object contains the display name of the stat as well as the value for the team.
```python
matchup = week_3.matchups[0]
print(f"{matchup.team1.name}\tvs\t{matchup.team2.name}")
for team1_stat, team2_stat in zip(matchup.team1_stats, matchup.team2_stats):
    print(f"{team1_stat.value}\t{team1_stat.display}\t{team2_stat.value}")
```

The full sequence of these examples can be run in the examples folder under the `readme.py` script, like so:
```
$ cd examples
$ yahoofantasy login
$ python readme.py
```

## Development

Issues, pull requests, and contributions are more than welcome.

To run the tests, after install:
```bash
$ py.test
```

Or to keep running tests using testmon and drop into a pdb shell on failure (my preferred mode):
```bash
$ pytest-watch --pdb -- --testmon -s
```
