import requests
from flask import request

STEAM_API_KEY = '26089045DDC2DD8258EB919713DE68DA'

def generate_steam_openid_url():
    steam_openid_url = (
        "https://steamcommunity.com/openid/login?"
        "openid.ns=http://specs.openid.net/auth/2.0&"
        "openid.mode=checkid_setup&"
        "openid.identity=http://specs.openid.net/auth/2.0/identifier_select&"
        "openid.claimed_id=http://specs.openid.net/auth/2.0/identifier_select&"
        "openid.return_to=http://localhost:5000/steam/callback"
    )
    return steam_openid_url

def handle_steam_login_callback(openid_params):
    """
    Handle OpenID login callback and validate the Steam ID.
    """
    openid_mode = openid_params.get('openid.mode')
    claimed_id = openid_params.get('openid.claimed_id')

    if openid_mode == 'id_res':
        steam_id = claimed_id.split('/')[-1]  # Extract Steam ID from claimed_id
        return steam_id
    return None