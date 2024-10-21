import requests
from flask import request

STEAM_API_KEY = '26089045DDC2DD8258EB919713DE68DA'

def handle_steam_callback():
    steam_id = request.args.get('openid.claimed_id')
    
    if steam_id:
        print(f"User logged in with Steam ID: {steam_id}")
        user_info, games = fetch_user_info(steam_id, STEAM_API_KEY)  # Corrected call
        display_user_info(user_info, games)
        return "Logged in successfully! You can close this window now.", 200
    else:
        return "Failed to log in.", 400

def fetch_user_info(steam_id, api_key):
    # Fetch user details
    player_summary_url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steam_id}"
    response = requests.get(player_summary_url)
    player_data = response.json()

    # Check for successful API response
    if 'response' in player_data and 'players' in player_data['response'] and player_data['response']['players']:
        player = player_data['response']['players'][0]
    else:
        print("Error fetching player data:", player_data)
        return None, []

    # Fetch owned games
    owned_games_url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_id}&include_appinfo=true&include_played_free_games=true"
    response = requests.get(owned_games_url)
    games_data = response.json()

    # Check for successful API response
    if 'response' in games_data and 'games' in games_data['response']:
        games = games_data['response']['games']
    else:
        print("Error fetching games data:", games_data)
        games = []

    return player, games

def display_user_info(user_info, games):
    if user_info:
        print(f"User Info: {user_info}")
        print("Owned Games:")
        for game in games:
            print(f"{game['name']} - Hours Played: {game['playtime_forever'] // 60} hours")
    else:
        print("No user info available.")
