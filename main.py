import customtkinter as ctk
import webbrowser
from flask import Flask, request, redirect
from threading import Thread
from Registration import open_registration_window
from database import create_user_table, verify_user_credentials

# Initialize database
create_user_table()

def button_signin():
    # Create a new window
    signin_window = ctk.CTkToplevel()
    signin_window.title("Sign In")
    signin_window.geometry("400x400")

    # Make the signin window stay on top of the main window
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

    # Sign-In Button
    signin_button = ctk.CTkButton(signin_window, text="Sign In", fg_color="red", command=on_signin)
    signin_button.pack(padx=10, pady=10)

def display_tabs():
    # Hide the sign-in and register buttons
    signIn.pack_forget()
    registerUser.pack_forget()
    title.pack_forget()

    # Create CTkTabview for switching between client platforms
    tabview = ctk.CTkTabview(app)
    tabview.pack(expand=True, fill="both", padx=20, pady=20)

    # Add gaming platform tabs
    tabview.add("Steam")
    tabview.add("PlayStation")
    tabview.add("Xbox")
    tabview.add("EA")
    tabview.add("Epic")
    tabview.add("GoG")

    # Steam tab content with OAuth button
    steam_button = ctk.CTkButton(tabview.tab("Steam"), text="Steam OAuth Sign-In", fg_color="red", command=steam_login)
    steam_button.pack(padx=10, pady=10)
    
    # PlayStation tab content with OAuth button
    playstation_button = ctk.CTkButton(tabview.tab("PlayStation"), text="PlayStation OAuth Sign-In", fg_color="red", command=lambda: print("PlayStation OAuth sign-in"))
    playstation_button.pack(padx=10, pady=10)

    # Xbox tab content with OAuth button
    xbox_button = ctk.CTkButton(tabview.tab("Xbox"), text="Xbox OAuth Sign-In", fg_color="red", command=lambda: print("Xbox OAuth sign-in"))
    xbox_button.pack(padx=10, pady=10)

    # EA tab content with OAuth button
    ea_button = ctk.CTkButton(tabview.tab("EA"), text="EA OAuth Sign-In", fg_color="red", command=lambda: print("EA OAuth sign-in"))
    ea_button.pack(padx=10, pady=10)

    # Epic tab content with OAuth button
    epic_button = ctk.CTkButton(tabview.tab("Epic"), text="Epic OAuth Sign-In", fg_color="red", command=lambda: print("Epic OAuth sign-in"))
    epic_button.pack(padx=10, pady=10)

    # GoG tab content with OAuth button
    gog_button = ctk.CTkButton(tabview.tab("GoG"), text="GoG OAuth Sign-In", fg_color="red", command=lambda: print("GoG OAuth sign-in"))
    gog_button.pack(padx=10, pady=10)

# Steam Login and Oauth
# Initialize Flask
app = Flask(__name__)

def run_flask():
    app.run(port=5000)

@app.route('/steam/callback')
def steam_callback():
    steam_id = request.args.get('openid.claimed_id')  # Adjust based on your request handling
    if steam_id:
        print(f"User logged in with Steam ID: {steam_id}")
        # You can update the UI or save the Steam ID
        return "Logged in successfully! You can close this window now.", 200
    else:
        return "Failed to log in.", 400

def steam_login():
    # Generate the Steam OpenID URL
    steam_openid_url = "https://steamcommunity.com/openid/login?" \
                       "openid.ns=http://specs.openid.net/auth/2.0&" \
                       "openid.mode=checkid_setup&" \
                       "openid.identity=http://specs.openid.net/auth/2.0/identifier_select&" \
                       "openid.claimed_id=http://specs.openid.net/auth/2.0/identifier_select&" \
                       "openid.return_to=http://localhost:5000/steam/callback"

    # Open the Steam login page in the default web browser
    webbrowser.open(steam_openid_url)

# App Frame
app = ctk.CTk()
app.geometry("1920x1080")
app.title("Chariots Game Reporter")

# Adding UI Elements
title = ctk.CTkButton(app, corner_radius=15, fg_color="red", text="Sign into your Account or Register a new account! ", text_color="White", font=ctk.CTkFont(family="Helvetica", size=18, weight="bold"))
title.pack(padx=10, pady=10)
title.configure(state='disabled')

# Sign in Button
signIn = ctk.CTkButton(app, corner_radius=15, text="Sign In", fg_color="red", command=button_signin)
signIn.pack(padx=10, pady=10)

# Register Button
registerUser = ctk.CTkButton(app, corner_radius=15, border_width=2, text="Register User", fg_color="red", command=lambda: open_registration_window(app))
registerUser.pack(padx=20, pady=20)

# Run app
app.mainloop()