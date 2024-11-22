import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageEnhance  # Importing PIL for image handling
import pygame
import random

# Initialize main window
root = tk.Tk()
root.title("Number Guessing Game")
root.geometry("1000x1000")
root.resizable(False, False)

# Global variables
random_num = 0
attempts_left = 0

pygame.mixer.init()
     

click_sound = pygame.mixer.Sound("click.wav")  # Replace with your sound file
win_sound = pygame.mixer.Sound("win.wav")
lose_sound = pygame.mixer.Sound("lose.wav")
game_overr = pygame.mixer.Sound("game_over.wav")
bg_sound = pygame.mixer.Sound("game_bg.wav")

#set sound volume
click_sound.set_volume(1.0)
win_sound.set_volume(0.5)
lose_sound.set_volume(0.5)
game_overr.set_volume(0.7)
bg_sound.set_volume(0.4)
# Load and modify the background image for reduced opacity
original_image = Image.open("background.png")  # Replace with your image file
opacity_adjuster = ImageEnhance.Brightness(original_image.convert("RGBA"))
transparent_image = opacity_adjuster.enhance(0.5)  # Reduce brightness for opacity
background_photo = ImageTk.PhotoImage(transparent_image)

# Create a Canvas widget to display the background
canvas = tk.Canvas(root, highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Display the background image
background_image_id = canvas.create_image(0, 0, image=background_photo, anchor="nw")

# Adjust the image size on window resize
def resize_image(event):
    global background_photo
    new_width = event.width
    new_height = event.height
    resized_image = transparent_image.resize((new_width, new_height), Image.ANTIALIAS)
    background_photo = ImageTk.PhotoImage(resized_image)
    canvas.itemconfig(background_image_id, image=background_photo)

# Bind the resize event to update the image
root.bind("<Configure>", resize_image)

# Set the sounds
def play_sound(sound):
    pygame.mixer.Sound.play(sound)


# Function to start the game
def start_game():
    play_sound(click_sound)
    play_sound(bg_sound)
    global random_num, attempts_left
    
    try:
        lower = int(lower_limit_entry.get())
        upper = int(upper_limit_entry.get())
        attempts_left = int(attempts_entry.get())
        attempt_limit = (upper - lower) // 2

        if lower >= upper:
            raise ValueError("Lower limit must be less than upper limit.")
        if attempts_left <= 0:
            raise ValueError("Attempts must be greater than 0.")
        if upper - lower == 1:
            if attempts_left > 1:
                raise Exception("You need to attempt only once!")
        elif attempts_left >= attempt_limit:
            raise Exception(f"Attempts must be less than {attempt_limit}")

        random_num = random.randint(lower, upper)
        feedback_label.config(text="Game started! Guess the number.")
        guess_entry.config(state="normal")
        guess_button.config(state="normal")
        start_button.config(state="disabled")

    except ValueError as e:
        play_sound(lose_sound)
        messagebox.showerror("Input Error", f"Invalid Input: {e}")
        
    except Exception as a:
        play_sound(lose_sound)
        messagebox.showerror("Attempt Limit Exceeded", a)
        


# Function to handle guesses
def check_guess():
    play_sound(click_sound)
    global attempts_left
    try:
        user_guess = int(guess_entry.get())
        attempts_left -= 1

        if user_guess == random_num:
            play_sound(win_sound)
            messagebox.showinfo("Congratulations!", f"You guessed it right! The number was {random_num}")
           
            reset_game()
        elif attempts_left == 0:
            play_sound(lose_sound)
            messagebox.showwarning("Game Over", f"Better Luck Next Time! The number was {random_num}")
            reset_game()
        else:
            hint = "greater than" if user_guess > random_num else "less than"
            feedback_label.config(text=f"Wrong! Hint: Your guess is {hint} the number.")
            attempts_label.config(text=f"Attempts left: {attempts_left}")

    except ValueError:
        play_sound(lose_sound)
        messagebox.showerror("Input Error", "Please enter a valid number.")
        


# Function to reset the game
def reset_game():
    play_sound(click_sound)
    guess_entry.delete(0, tk.END)
    guess_entry.config(state="disabled")
    guess_button.config(state="disabled")
    start_button.config(state="normal")
    feedback_label.config(text="Game reset! Enter range and attempts to start again.")
    attempts_label.config(text="")


# Function to center the widgets
def center_window(window, widget, y_offset):
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    widget_width = widget.winfo_width()
    widget_height = widget.winfo_height()
    
    x_pos = (window_width - widget_width) // 2
    y_pos = y_offset
    
    window.create_window(x_pos, y_pos, window=widget)


# Layout with proper alignment
title_label = tk.Label(root, text="Number Guessing Game", font=('Arial', 20, "bold"), bg="white")
canvas.create_window(500, 50, window=title_label)

# Lower Limit
lower_limit_label = tk.Label(root, text="Lower Limit:", font=('Arial', 12), bg="white")
canvas.create_window(300, 150, window=lower_limit_label)
lower_limit_entry = tk.Entry(root, font=('Arial', 12), width=10)
canvas.create_window(500, 150, window=lower_limit_entry)

# Upper Limit
upper_limit_label = tk.Label(root, text="Upper Limit:", font=('Arial', 12), bg="white")
canvas.create_window(300, 200, window=upper_limit_label)
upper_limit_entry = tk.Entry(root, font=('Arial', 12), width=10)
canvas.create_window(500, 200, window=upper_limit_entry)

# Number of Attempts
attempts_label = tk.Label(root, text="Number of Attempts:", font=('Arial', 12), bg="white")
canvas.create_window(300, 250, window=attempts_label)
attempts_entry = tk.Entry(root, font=('Arial', 12), width=10)
canvas.create_window(500, 250, window=attempts_entry)

# Start Button
start_button = tk.Button(root, text="Start Game", command=start_game, bg="green", fg="white", font=("Arial", 12))
canvas.create_window(500, 300, window=start_button)

# Feedback label
feedback_label = tk.Label(root, text="Enter the range and attempts to start!", font=("Arial", 12), bg="white")
canvas.create_window(500, 350, window=feedback_label)

# Guess input
guess_label = tk.Label(root, text="Your Guess:", font=('Arial', 12), bg="white")
canvas.create_window(300, 400, window=guess_label)
guess_entry = tk.Entry(root, font=('Arial', 12), width=10, state="disabled")
canvas.create_window(500, 400, window=guess_entry)

# Guess Button
guess_button = tk.Button(root, text="Submit Guess", command=check_guess, state="disabled", bg="light blue", fg="white")
canvas.create_window(500, 450, window=guess_button)

# Reset Button
reset_button = tk.Button(root, text="Reset Game", command=reset_game, bg="red", fg="black", font=("Arial", 12))
canvas.create_window(500, 500, window=reset_button)

# Run the main loop
root.mainloop()

