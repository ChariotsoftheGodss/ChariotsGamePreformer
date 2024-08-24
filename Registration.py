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

        if password == confirm_password:
            register_user(email, username, password)  # Remove confirm_password from this call
            print(f"Registered new user: {username} with email: {email}")
            register_window.destroy()  # Close the window after registration
        else:
            print("Passwords do not match!")

    # Register button (make sure it's created in the right scope)
    register_button = ctk.CTkButton(register_window, text="Register", fg_color="red", command=on_register)
    register_button.pack(padx=10, pady=10)
