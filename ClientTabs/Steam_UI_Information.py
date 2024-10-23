import customtkinter as ctk
import webbrowser
import requests
from Oauth.steam_auth import generate_steam_openid_url, STEAM_API_KEY

class SteamUI:
    def __init__(self, tabview):
        self.tabview = tabview
        self.steam_frame = self.create_steam_frame()

    def create_steam_frame(self):
        # Create a frame in the Steam tabv
        steam_frame = ctk.CTkFrame(self.tabview.tab("Steam"))
        steam_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Create the Steam login button
        self.steam_login_button = ctk.CTkButton(steam_frame, text="Login with Steam", fg_color="red", command=self.steam_login)
        self.steam_login_button.pack(side="top", padx=10, pady=10)

        return steam_frame

    def steam_login(self):
        # Destroy the steam login button on click
        self.steam_login_button.destroy()

        # Open Steam page & login
        openid_url = generate_steam_openid_url()
        webbrowser.open(openid_url)

        # Create and pack the game box and hours label after login button is destroyed to display user information in
        self.create_game_box_and_label()

    def create_game_box_and_label(self):
        # Create the Frame for games to be seen
        self.game_box = ctk.CTkFrame(self.steam_frame)
        self.game_box.pack(side="top", padx=10, pady=10, fill="both", expand=True)

        # Label to display hours played
        self.hours_label = ctk.CTkLabel(self.steam_frame, text="Hours Played: ")
        self.hours_label.pack(side="top", padx=10, pady=10)

    def handle_user_data(self, steam_id):
        # Fetch owned games and user information
        games = self.get_owned_games(steam_id)
        
        # Populate the Frame with games
        for game in games:
            self.game_box.insert("end", game['name'])  # Insert game names into the box

        # Set up a callback to update the hours label when a game is selected
        self.game_box.bind("<<ListboxSelect>>", self.on_game_select)

    def get_owned_games(self, steam_id):
        # Use GetOwnedGames API to get the list of owned games
        url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
        params = {
            'key': STEAM_API_KEY,
            'steamid': steam_id,
            'include_appinfo': True,  # To include game names
            'include_played_free_games': True,  # Include free games
            'format': 'json'
        }

        # Make the API request
        response = requests.get(url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            if 'response' in data and 'games' in data['response']:
                games = data['response']['games']
                # Create a list of games with their name and playtime
                game_list = [{'name': game['name'], 'appid': game['appid'], 'playtime_forever': game['playtime_forever']} for game in games]
                return game_list
            else:
                print("No games found for this user.")
                return []
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []

    def on_game_select(self, event):
        selected_index = self.game_box.curselection()
        if selected_index:
            selected_game = self.game_box.get(selected_index)  # Get the selected game name
            hours_played = self.get_hours_played(selected_game)  # Fetch hours based on selected game & display
            self.hours_label.config(text=f"Hours Played: {hours_played}")

    def get_hours_played(self, selected_game):
        # Fetch the App ID from the game data
        app_id = self.get_app_id(selected_game)  # Get the App ID based on the game name
        if app_id and hasattr(self, 'steam_id'):
            played_forever = self.get_played_forever(self.steam_id, app_id)
            return played_forever / 60 
        return 0

    def get_app_id(self, game_name):
        # Retrieve the App ID based on game name
        return next((game['appid'] for game in self.games if game['name'] == game_name), None)

