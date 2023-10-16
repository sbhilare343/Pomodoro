import math
import pygame
from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
time_reset = 0


# ---------------------------- Sound ------------------------------- #
def set_alarm():
    pygame.mixer.init()
    pygame.mixer.music.load("Alarm.mp3")
    pygame.mixer.music.play()
    pygame.time.wait(2000)
    pygame.mixer.quit()


# ---------------------------- TIMER RESET ------------------------------- #
def reset():
    window.after_cancel(time_reset)
    canvas.itemconfig(timer, text="00:00")
    Timer_label.config(text="Timer")
    tick_label.config(text="")
    global reps
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #
def timer_mech():
    global reps
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    reps += 1
    if reps % 8 == 0:
        Timer_label.config(text="Long Break", fg=RED, bg=YELLOW)
        count_down(long_break_sec)
    elif reps % 2 == 0:
        Timer_label.config(text="Short Break", fg=PINK, bg=YELLOW)
        count_down(short_break_sec)
    else:
        Timer_label.config(text="Work", fg=GREEN, bg=YELLOW)
        count_down(work_sec)
    set_alarm()


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    count_minute = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = "0" + str(count_sec)

    canvas.itemconfig(timer, text=f"{count_minute}:{count_sec}")
    if count > 0:
        global time_reset
        time_reset = window.after(1000, count_down, count - 1)
    else:
        timer_mech()
        marks = ""
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            marks += "✔"
        tick_label.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=50, pady=50, bg=YELLOW)

# Canvas window
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")  # to convert to PhotoImage type
# print(type(tomato_img))
canvas.create_image(100, 112, image=tomato_img)
timer = canvas.create_text(100, 118, text="00:00", fill="white", font=(FONT_NAME, 20))
canvas.grid(row=1, column=1)

# Timer label
Timer_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 24))
Timer_label.grid(row=0, column=1)

# Tick mark label
tick = ""
tick_label = Label(text=tick, bg=YELLOW, fg=GREEN)
tick_label.grid(row=3, column=1)

# Buttons
button1 = Button(text="Start", highlightthickness=0, bg=YELLOW, command=timer_mech)
button1.grid(row=2, column=0)

button2 = Button(text="Reset", highlightthickness=0, bg=YELLOW, command=reset)
button2.grid(row=2, column=2)

window.mainloop()
