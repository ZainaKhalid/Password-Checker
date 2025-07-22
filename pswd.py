import tkinter as tk
from tkinter import messagebox
import re
import random
import hashlib
import requests

# Function to generate a strong password
def generate_strong_password():
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*?"
    return "".join(random.sample(characters, 12))

# Function to check password strength
def check_password_strength(password):
    strength = 0
    remarks = ""

    if len(password) >= 8:
        strength += 1
    if re.search(r'[A-Z]', password):
        strength += 1
    if re.search(r'[a-z]', password):
        strength += 1
    if re.search(r'\d', password):
        strength += 1
    if re.search(r'[@$!%*?&]', password):
        strength += 1

    common_passwords = ["123456", "password", "qwerty", "12345678", "abc123"]
    if password in common_passwords:
        strength = 0
        remarks = "Too common! Choose a stronger password."

    if strength == 0:
        remarks = "Very Weak"
    elif strength == 1 or strength == 2:
        remarks = "Weak"
    elif strength == 3:
        remarks = "Medium"
    elif strength == 4:
        remarks = "Strong"
    elif strength == 5:
        remarks = "Very Strong"

    if strength <= 2:
        return remarks, f"Suggested Password: {generate_strong_password()}"

    return remarks, None

# Function to check password leaks
def check_password_leak(password):
    sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)

    leaked_passwords = response.text.splitlines()
    for line in leaked_passwords:
        leaked_suffix, count = line.split(":")
        if leaked_suffix == suffix:
            return f"⚠️ This password has been leaked {count} times! Change it."

    return "✅ This password is safe!"

# Function to handle button click
def evaluate_password():
    password = password_entry.get()
    if not password:
        messagebox.showerror("Error", "Please enter a password!")
        return
    
    strength, suggestion = check_password_strength(password)
    leak_result = check_password_leak(password)

    result_message = f"Strength: {strength}\n{leak_result}"
    if suggestion:
        result_message += f"\n{suggestion}"

    messagebox.showinfo("Password Check Result", result_message)

# GUI setup
root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("400x300")

tk.Label(root, text="Enter Password:", font=("Arial", 12)).pack(pady=10)
password_entry = tk.Entry(root, show="*", width=30, font=("Arial", 12))
password_entry.pack(pady=5)

check_button = tk.Button(root, text="Check Password", command=evaluate_password, font=("Arial", 12))
check_button.pack(pady=10)

# Run Tkinter
root.mainloop()
