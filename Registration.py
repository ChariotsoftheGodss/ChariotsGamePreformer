import re
import customtkinter as ctk
from database import register_user

def open_registration_window(app):
    # Create a new window (subwindow)
    register_window = ctk.CTkToplevel()
    register_window.title("Register New User")
    register_window.geometry("400x800")

    # Make the register window stay on top of the main window
    register_window.transient(app)
    register_window.grab_set()

    # Register UI Elements
    label_email = ctk.CTkLabel(register_window, text="Email:")
    label_email.pack(padx=10, pady=5)
    entry_email = ctk.CTkEntry(register_window)
    entry_email.pack(padx=10, pady=5)

    label_username = ctk.CTkLabel(register_window, text="Username:")
    label_username.pack(padx=10, pady=5)
    entry_username = ctk.CTkEntry(register_window)
    entry_username.pack(padx=10, pady=5)

    label_password = ctk.CTkLabel(register_window, text="Password:")
    label_password.pack(padx=10, pady=5)
    entry_password = ctk.CTkEntry(register_window, show="*")
    entry_password.pack(padx=10, pady=5)

    label_confirm_password = ctk.CTkLabel(register_window, text="Confirm Password:")
    label_confirm_password.pack(padx=10, pady=5)
    entry_confirm_password = ctk.CTkEntry(register_window, show="*")
    entry_confirm_password.pack(padx=10, pady=5)

    # Register user when button is clicked
    def on_register():
        email = entry_email.get()
        username = entry_username.get()
        password = entry_password.get()
        confirm_password = entry_confirm_password.get()

        # Email Validation regex
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

         # Password complexity check
        password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

        # Validate email is an email
        if not re.match(email_regex, email):
            print("Invalid email format!")
            return
        
        # Validate password Complexity for Security
        if not re.match(password_regex, password):
            print("Password must be at least 8 characters long and include at least 1 uppercase letter, 1 lowercase letter, 1 number, and 1 special character.")
            return
        
          # Check if passwords match
        if password != confirm_password:
            print("Passwords do not match!")
            return
        
        # If all good, then regiser the user
        register_user(email, username, password)
        print(f"Registered new user: {username} with email: {email}")
        register_window.destroy() # Close the window


    # Register button (make sure it's created in the right scope)
    register_button = ctk.CTkButton(register_window, text="Register", fg_color="red", command=on_register)
    register_button.pack(padx=10, pady=10)
