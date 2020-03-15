# Yahoo Fantasy API Wrapper

The Yahoo Fantasy Sports API is difficult to comprehend, has [this strange one-page documentation setup](https://developer.yahoo.com/fantasysports/guide/) that is hard to navigate, and seems to only want to conform to a small portion of the OAuth spec. This library/SDK makes your life easier if you want to write an app that interfaces with the Yahoo Fantasy Sports API.

## Installation

```
pip install yahoofantasy
```

You will also need a application registered on the [Yahoo Developer Site](https://developer.yahoo.com/apps/). You'll need your client ID and secret. The app just needs to have read permissions.

## Basic Usage

You're going to want to start off by creating a context, providing your credentials and your refresh token. This context is where all of your API requests will originate and league information will live.

```python
from yahoofantasy import Context

ctx = Context(my_client_id, my_client_secret, my_refresh_token)
```

You can start by inspecting what leagues you are a part of:
```python
leagues = ctx.get_leagues('mlb', 2020)
for league in leagues:
    print(league.name + " -- " + league.league_type)
```
