# 🏆 Yahoo Fantasy API Wrapper 🏆

The Yahoo Fantasy Sports API is difficult to comprehend, has [this strange one-page documentation setup](https://developer.yahoo.com/fantasysports/guide/) that is hard to navigate, and seems to only want to conform to a small portion of the OAuth spec. This library/SDK makes your life easier if you want to write an app that interfaces with the Yahoo Fantasy Sports API.

This library will work for any Yahoo Fantasy Sports API leagues/teams. It contains some common constructs and helper methods for head-to-head leagues for the NFL 🏈, MLB ⚾, NHL 🏒 and NBA 🏀.

## Table of Contents

* [Installation](#installation)
* [Basic Usage](#basic-usage)
* [Authentication](#authentication)
* [Concepts](#concepts)
* [Command Line (CLI)](#command-line-cli)
* [Development](#development)

## Installation

```
pip install yahoofantasy
```

You will also need a application registered on the [Yahoo Developer Site](https://developer.yahoo.com/apps/). You'll need your client ID and secret. The app just needs to have read permissions. See below for instructions on how to set up your Yahoo Developer application if you don't have one already.

## Basic Usage

You're going to want to start off by logging in to your Yahoo Developer application, then creating a context. This context is where all of your API requests will originate and league information will live.

```bash
yahoofantasy login
```

Once you've logged in, create a context and use that to make requests. For example, to fetch all of your leagues for a given game/season:
```python
from yahoofantasy import Context

ctx = Context()
leagues = ctx.get_leagues('mlb', 2020)
for league in leagues:
    print(league.name + " -- " + league.league_type)
```

## Authentication

You can use the built-in `yahoofantasy` CLI to obtain an access token and refresh token for your application. Follow these steps:

1. Set up your Yahoo application to have a callback/redirect URI of `https://localhost:8000`. If you already have an app that points to your local host on a different port or different path that's ok, you can customize later on.
2. Install `yahoofantasy` if you haven't already
```bash
pip install yahoofantasy
```
3. Log in with your Yahoo account. This command will launch a browser that will ask you to authenticate to your app. It will then store the token in a local file that can be consumed by the yahoofantasy SDK.
```bash
yahoofantasy login
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

* A **League** will contain multiple **Player** objects.
```python
from yahoofantasy import League

league = League(ctx, '388.l.25000')  # Use a manual league ID or get it from league.id above
for player in league.players():
    print(f"{player.name.full} - {player.display_position} - {player.editorial_team_abbr}")
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
for team in league.teams():
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
cd examples
yahoofantasy login
python readme.py
```

## Command Line (CLI)

This package comes with a built in CLI to let you do some handy tasks without writing any Python code. This is useful for exporting a spreadsheet with trades in your league, player performances, etc and doing some separate analysis on them.

### General Properties

Each CLI command has these common properties/arguments to let you control its behavior

* **-g/--game** - which sport you are exporting (e.g., nfl, mlb)
* **-s/--season** - which season you are exporting (e.g., 2020, 2019, etc)
* **-o/--output** - the filename of the CSV to write to, defaults to `stdout` which prints to stdout instead of to a file

If you don't provide these parameters you will be prompted for the required ones when you run your command. 
These parameters must be provided after the `dump` command but before the type of export you want to complete. For example:
```bash
yahoofantasy dump -g nfl -s 2020 -o path/to/output.csv performances
```

### Types of Exports

#### Player Performances

Dumps a CSV with every player that was owned for every week and their stats.

```bash
yahoofantasy dump performances
```

Simplified output example:
| name | week | manager | position | points | Pass TD | Rush Yds |
|-|-|-|-|-|-|-|
| Drew Brees | 1 | Manager Name | QB | 16.4 | 2 | 2 |
| Dalvin Cook | 1 | Manager | RB | 21.3 | 0 | 50 |

#### Matchups

In a head-to-head league, a CSV dump of all manager matchups from the season

```bash
yahoofantasy dump matchups
```

Simplified output example:
| week | manager | win | points | proj_points | opponent | opp_points | opp_proj_points |
|-|-|-|-|-|-|-|-|
| 1 | Manager 1 | False | 90.0 | 133.55 | Manager 2 | 142.68 | 136.79 |
| 1 | Manager 2 | True | 142.68 | 136.79 | Manager 1 | 90.0 | 133.55 |

#### Draft Results

A CSV dump of every draft pick

```bash
yahoofantasy dump draftresults
```

Simplified output example:
| pick | round | manager | player | pos |
|-|-|-|-|-|
| 1 | 1 | Manager 1 | Christian McCaffrey | RB |
| 2 | 1 | Manager 2 | Saquon Barkley | RB |

#### Transactions

A CSV dump of every transaction made for a season. Includes trades, adds, drops, and commissioner moves

```bash
yahoofantasy dump transactions
```

Simplified output example:
| type | player_type | player | from | to | ts | week_idx | bid |
|-|-|-|-|-|-|-|-|
| drop | drop | Damien Harris | Elementary Mr Watson | waivers | 09/09/2020, 20:57:15 | 36 |  |
| add/drop | add | James Robinson | waivers | Kittles taste the ðŸŒˆ | 09/11/2020, 00:22:20 | 36 |  |

### Shell (Python interpreter)

A command is available to drop you into a Python interpreter with access to your `Context` object as the `ctx` variable. From the directory where you ran `yahoofantasy login` you can run:

```bash
yahoofantasy shell
```

### Clearing cache

The yahoofantasy library maintains its own persisted cache of certain Yahoo! API responses. This cuts down on the number of requests that need to be made and makes future function calls faster. Occasionally you may want to clear this cache but not lose your authentication data. You can do so by running the following CLI command from your yahoofantasy project directory:

```bash
yahoofantasy clear-cache
```

## Development

Issues, pull requests, and contributions are more than welcome.

### Unit Tests
To run the tests, after install:
```bash
py.test
```

Or to keep running tests using testmon and drop into a pdb shell on failure (my preferred mode):
```bash
pytest-watch --pdb -- --testmon -s
```

### Releasing
I use [bump2version](https://github.com/c4urself/bump2version) to manage version bumping. This will update the version number in the library, commit it, and create a version tag.

```bash
bump2version minor
git push
```
