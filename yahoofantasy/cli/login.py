import click
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import requests
from time import time
from urllib.parse import urlparse, parse_qs, urlencode
import webbrowser

from .utils import error, success
from yahoofantasy.context import YAHOO_OAUTH_URL
from yahoofantasy.util.persistence import save, load, get_persistence_filename

ACCESS_CODE = None


@click.command()
@click.option('--client-id', default='', help='Yahoo App Client ID')
@click.option('--client-secret', default='', help='Yahoo App Client Secret')
@click.option('--redirect-uri', default='http://localhost:8000', help='Redirect URI')
@click.option('--listen-port', default='8000', type=int, help='Port to listen on')
@click.option('--persist-key', default='', help='Persistence Key')
def login(client_id, client_secret, redirect_uri, listen_port, persist_key):
    global ACCESS_CODE
    persisted_auth_data = load('auth', default={}, ttl=-1, persist_key=persist_key)
    client_id = (
        client_id
        or os.environ.get('YAHOO_CLIENT_ID')
        or persisted_auth_data.get('client_id')
        or click.prompt('Yahoo Client ID')
    )
    client_secret = (
        client_secret
        or os.environ.get('YAHOO_CLIENT_SECRET')
        or persisted_auth_data.get('client_secret')
        or click.prompt('Yahoo Client Secret')
    )

    if not client_id or not client_secret:
        error("Must provide client ID and client secret", exit=True)

    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
    }
    ACCESS_CODE = None
    url = YAHOO_OAUTH_URL + '/request_auth?' + urlencode(params)
    click.echo("Launching browser for Yahoo authentication. If this doesn't work use "
               "this link manually:")
    click.echo(url)
    webbrowser.open_new_tab(url)
    click.echo("Launching OAuth handler server on localhost:{}".format(listen_port))
    server = HTTPServer(('', listen_port), Handler)
    server.handle_request()
    if not ACCESS_CODE:
        error("Couldn't determine access code from URL string", exit=True)
    click.echo("Access code: {}".format(ACCESS_CODE))
    click.echo("Fetching access token...")
    resp = requests.post(YAHOO_OAUTH_URL + '/get_token', data={
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'code': ACCESS_CODE,
        'redirect_uri': 'oob',
    })
    try:
        body = resp.json()
        access_token = body.get('access_token')
        access_token_expires = time() + body.get('expires_in')
        refresh_token = body.get('refresh_token')
    except Exception:
        error("Couldn't get access token or refresh token", exit=True)

    persist_file = get_persistence_filename(persist_key)
    success("Access token retrieved!. This will be persisted at {}".format(persist_file))
    save('auth', {
        'client_id': client_id,
        'client_secret': client_secret,
        'access_token': access_token,
        'access_token_expires': access_token_expires,
        'refresh_token': refresh_token,
    }, persist_key=persist_key)
    click.echo("Access Token : {}".format(access_token))
    click.echo("Refresh Token: {}".format(refresh_token))


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        global ACCESS_CODE
        try:
            access_code = parse_qs(urlparse(self.path).query)['code'][0]
            ACCESS_CODE = access_code
        except Exception:
            print("Couldn't find the access code in the query string....")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write("Got it! You may close this tab now".encode())

    def log_message(self, format, *args):
        return
