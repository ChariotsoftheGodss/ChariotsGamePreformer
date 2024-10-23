import customtkinter as ctk
from flask import Flask, request
from threading import Event, Thread
from Registration import open_registration_window
from database import create_user_table, verify_user_credentials
from Oauth.steam_auth import STEAM_API_KEY, handle_steam_login_callback
from ClientTabs.Steam_UI_Information import SteamUI  # Import the new Steam UI class

# Initialize Flask
flask_app = Flask(__name__)

# Initialize database
create_user_table()

# Event to stop the Flask server thread
shutdown_event = Event()

# App Frame
app = ctk.CTk()
app.geometry("1920x1080")
app.title("Chariots Game Reporter")

# UI Title Element
title = ctk.CTkButton(app, corner_radius=15, fg_color="red", text="Sign into your Account or Register a new account! ", text_color="White", font=ctk.CTkFont(family="Helvetica", size=18, weight="bold"))
title.pack(padx=10, pady=10)
title.configure(state='disabled')

# Register Button
registerUser = ctk.CTkButton(app, corner_radius=15, border_width=2, text="Register User", fg_color="red", command=lambda: open_registration_window(app))
registerUser.pack(padx=20, pady=20)

#Initial Sign-in Button
def button_signin():
    # Create a new window
    signin_window = ctk.CTkToplevel()
    signin_window.title("Sign In")
    signin_window.geometry("400x400")

    # Make the signin window stay on top of the main window until done
    signin_window.transient(app)
    signin_window.grab_set()

    # Sign-In UI Elements
    label_email = ctk.CTkLabel(signin_window, text="Email:")
    label_email.pack(padx=10, pady=5)
    entry_email = ctk.CTkEntry(signin_window)
    entry_email.pack(padx=10, pady=5)

    label_password = ctk.CTkLabel(signin_window, text="Password:")
    label_password.pack(padx=10, pady=5)
    entry_password = ctk.CTkEntry(signin_window, show="*")
    entry_password.pack(padx=10, pady=5)

    # Sign-In logic
    def on_signin():
        email = entry_email.get()
        password = entry_password.get()

        if verify_user_credentials(email, password):
            print(f"User {email} signed in successfully!")
            signin_window.destroy()  # Close the window after successful sign-in
            display_tabs()  # Show the client tabs
        else:
            print("Invalid email or password!")

    # Sign-In Button for logic
    signin_button = ctk.CTkButton(signin_window, text="Sign In", fg_color="red", command=on_signin)
    signin_button.pack(padx=10, pady=10)

# Sign in Button for Main Frame - Here due to logic
signIn = ctk.CTkButton(app, corner_radius=15, text="Sign In", fg_color="red", command=button_signin)
signIn.pack(padx=10, pady=10)

# Destroy Singing/Register buttons Display Client Tabs
def display_tabs():
    # Hide the sign-in and register buttons
    signIn.pack_forget()
    registerUser.pack_forget()
    title.pack_forget()

    # Create Tabview for switching between client platforms
    tabview = ctk.CTkTabview(app)
    tabview.pack(expand=True, fill="both", padx=20, pady=20)

    # Add gaming platform tabs
    tabview.add("Steam")
    tabview.add("PlayStation")
    tabview.add("Xbox")
    tabview.add("EA")
    tabview.add("Epic")
    tabview.add("GoG")

    # Add SteamUI functionality to Steam tab
    steam_ui = SteamUI(tabview)
    
# Callback handler for Steam OAuth
@flask_app.route('/steam/callback')
def steam_callback():
    openid_params = request.args.to_dict()
    steam_id = handle_steam_login_callback(openid_params)

    if steam_id:
        # Pass the steam_id to the SteamUI instance to handle user data
        steam_id.handle_user_data(steam_id)
        return "Successfully logged in!", 200
    else:
        return "Steam login failed.", 400

# Run Flask in a separate thread
def run_flask():
    while not shutdown_event.is_set():
        flask_app.run(port=5000, use_reloader=False)  # Auto-reloader to avoid multiple instances

if __name__ == "__main__":
    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Handle app closing
    def on_closing():
        shutdown_event.set()  # Signal the Flask thread to stop
        app.quit()  # Close the CustomTkinter app

    app.protocol("WM_DELETE_WINDOW", on_closing)  # Call on_closing when the app window is closed
    app.mainloop()
