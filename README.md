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

## Retreiving Access and Refresh Tokens

You can use the built-in `yahoofantasy` CLI to obtain an access token and refresh token for your application. Follow these steps:

1. Set up your Yahoo application to have a callback/redirect URI of `http://localhost:8000`. If you already have an app that points to your local host on a different port or different path that's ok, you can customize later on.
2. Install `yahoofantasy` if you haven't already
```bash
$ pip install yahoofantasy
```
3. Log in with your Yahoo account. This command will launch a browser that will ask you to authenticate to your app. It will then store the token in a local file that can be consumed by the yahoofantasy SDK.
```bash
$ yahoofantasy login
```

Try `yahoofantasy login --help` for some advanced options, like customizing the port or redirect URI
