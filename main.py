import tkinter as tk
from tkinter import messagebox
import random as random

from oeis_scraper import OEISFetcher


### Checks to see if input is an integer ###
def is_integer(n):
    try:
        int(n)
        return True
    except ValueError:
        return False


### Main window and a containing frame for the screens ###
window = tk.Tk()
screenContainer = tk.Frame(window)

oeis = OEISFetcher()
seq_length = 0

### Main Screen class for organizing data into pages to navigate in game ###
class Screen(tk.Frame):
    def __init__(self, submits=True, *args, **kwargs):
        super().__init__(screenContainer, *args, **kwargs)
        self.text = tk.StringVar()
        self.text.set("")
        self.label = tk.Label(self, textvariable=self.text, wraplength=1000)
        self.submits = submits
        if self.submits:
            self.entry = tk.Entry(self)
        self.button_frame = tk.Frame(self)
        self.input = ""
        self.buttonList = []

    def set_text(self, txt):
        self.text.set(txt)

    def get_input(self):
        if self.submits:
            self.input = self.entry.get()
            return self.input
        else:
            return 0

    def clear_text(self):
        if self.submits:
            self.entry.delete(0, 'end')
        else:
            return 0

    def add_button(self, *args, **kwargs):
        b = tk.Button(self, *args, **kwargs)
        self.buttonList.append(b)

    def make_visible(self):
        self.pack()
        self.label.pack()
        if self.submits:
            self.entry.pack()
        self.button_frame.pack()
        for b in self.buttonList:
            b.pack(side="top")

    def make_invisible(self):
        self.pack_forget()
        # self.label.pack_forget()
        # self.entry.pack_forget()
        # self.button_frame.pack_forget()


### Flip between two screens of the game ###
def toggleScreens(screen1, screen2):
    screen1.make_invisible()
    screen2.make_visible()
    screen1.clear_text()


### Set up start page ###
def begin_game():
    number = startScreen.get_input()
    if is_integer(number) and int(number) < 20:
        global seq_length
        seq_length = int(number)
        sequence = oeis.get_random_sequence()
        toggleScreens(startScreen, gameScreen)
        gameScreen.set_text("Guess the next entry in the sequence \n" + str(sequence[0:seq_length])[:-1][1:] + ", ...")
    else:
        messagebox.showerror("Error", "Please enter an integer less than 20.")

startScreen = Screen()
startText = "Welcome to the integer guessing game! Pick a number of entries to see from the sequence."
startScreen.set_text(startText)
startScreen.add_button(text="Start", command=begin_game)


### Main game page ###
def submit_guess():
    if is_integer(gameScreen.get_input()):
        guess = int(gameScreen.get_input())
        global seq_length
        if guess == oeis.sequence[seq_length]:
            toggleScreens(gameScreen, winScreen)
        else:
            toggleScreens(gameScreen, loseScreen)
    else:
        messagebox.showerror("Error", "Please enter integer")


gameScreen = Screen()
# gameScreen.add_button(text="Go Back", command=lambda: toggleScreens(gameScreen, startScreen))
gameScreen.add_button(text="Submit Guess", command=submit_guess)

### Winner page ###
def try_next():
    global seq_length
    seq_length += 1
    if seq_length <= len(oeis.sequence):
        toggleScreens(winScreen, gameScreen)
        gameScreen.set_text("Guess the next entry in the sequence \n" + str(oeis.sequence[0:seq_length])[:-1][1:] + ", ...")
    else:
        pass

winScreen = Screen(submits=False)
winScreen.set_text("Congratulations! Your guess was correct!")
winScreen.add_button(text="Try Next Number", command=try_next)
winScreen.add_button(text="New Sequence", command=lambda: toggleScreens(winScreen, startScreen))

### Loser page ###
def view_solutions(screen):
    toggleScreens(screen, solScreen)
    if len(oeis.sequence) > 50:
        solScreen.set_text("The solution is (first 50 terms): \n" + str(oeis.sequence[:50])[:-1][1:] + " \n with OEIS id " + str(oeis.id))
    else:
        solScreen.set_text("The solution is \n" + str(oeis.sequence)[:-1][1:] + " \n with OEIS id " + str(oeis.id))

loseScreen = Screen(submits=False)
loseScreen.set_text("Incorrect guess.")
loseScreen.add_button(text="Try Again", command=lambda: toggleScreens(loseScreen, gameScreen))
# loseScreen.add_button(text="Hint")
loseScreen.add_button(text="New Game", command=lambda: toggleScreens(loseScreen, startScreen))
loseScreen.add_button(text="Solution", command=lambda: view_solutions(loseScreen))

### Solution page ###
solScreen = Screen(submits=False)
solScreen.add_button(text="New Game", command=lambda: toggleScreens(solScreen, startScreen))



### Set up for gameplay ###
startScreen.make_visible()
screenContainer.pack()
window.mainloop()
