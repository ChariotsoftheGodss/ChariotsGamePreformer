import customtkinter as ctk
import tkinter.font as tkfont
from Registration import open_registration_window
from database import create_user_table, verify_user_credentials
from PIL import Image, ImageTk

# Initialize database
create_user_table()

def button_signin():
    # Create a new window (subwindow)
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

        if verify_user_credentials(password, email):
            print(f"User {email} signed in successfully!")
            signin_window.destroy()  # Close the window after successful sign-in
            display_gaming_buttons()  # Show the gaming client buttons
        else:
            print("Invalid email or password!")

    # Sign-In Button
    signin_button = ctk.CTkButton(signin_window, text="Sign In", fg_color="red", command=on_signin)
    signin_button.pack(padx=10, pady=10)

def display_gaming_buttons():
    # Hide the sign-in and register buttons
    signIn.pack_forget()
    registerUser.pack_forget()
    title.pack_forget()

    # Create the gaming buttons and add them to the frame
    steam_button = ctk.CTkButton(app, text="Steam", fg_color="red", corner_radius=0, command=lambda: print("Steam login"))
    steam_button.grid(row=0, column=0, padx=90, pady=10)

    playstation_button = ctk.CTkButton(app, text="PlayStation", fg_color="red", corner_radius=0, command=lambda: print("PlayStation login"))
    playstation_button.grid(row=0, column=1, padx=90, pady=10)

    xbox_button = ctk.CTkButton(app, text="Xbox", fg_color="red", corner_radius=0, command=lambda: print("Xbox login"))
    xbox_button.grid(row=0, column=2, padx=90, pady=10)

    ea_button = ctk.CTkButton(app, text="EA", fg_color="red", corner_radius=0, command=lambda: print("EA login"))
    ea_button.grid(row=0, column=3, padx=90, pady=10)

    epic_button = ctk.CTkButton(app, text="Epic", fg_color="red", corner_radius=0, command=lambda: print("Epic login"))
    epic_button.grid(row=0, column=4, padx=90, pady=10)

    gog_button = ctk.CTkButton(app, text="GoG", fg_color="red", corner_radius=0, command=lambda: print("GoG login"))
    gog_button.grid(row=0, column=5, padx=90, pady=10)
    
    
# App Frame
app = ctk.CTk()
app.geometry("1920x1080")
app.title("Chariots Game Reporter")

# Use Pillow to load the image
background_image = Image.open(r'C:\Users\Grant\Downloads\Designer.png')
background_image = background_image.resize((app.winfo_screenwidth(), app.winfo_screenheight()), Image.Resampling.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)

# Create a background image label
background_label = ctk.CTkLabel(app, corner_radius=0, image=background_photo, text="")
background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
# Keep a reference to the image to prevent garbage collection
background_label.image = background_photo

# Adding UI Elements
title = ctk.CTkButton(app, corner_radius=0, fg_color="red", text="Sign into your Account or Register a new account! ", text_color="White", font=ctk.CTkFont(family="Helvetica", size=18, weight="bold"))
title.pack(padx=10, pady=10)
title.configure(state='disabled')

# Sign in Button
signIn = ctk.CTkButton(app, corner_radius=0, text="Sign In", fg_color="red", command=button_signin)
signIn.pack(padx=10, pady=10)

# Register Button
registerUser = ctk.CTkButton(app, corner_radius=0, text="Register User", fg_color="red", command=lambda: open_registration_window(app))
registerUser.pack(padx=20, pady=20)

# Run app
app.mainloop()