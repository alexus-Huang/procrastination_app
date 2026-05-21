import tkinter as tk
import math
import json
import os
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pygetwindow as gw
from tkinter import ttk

APP_DIR = os.path.join(os.getenv("APPDATA"), "PomodoroApp")
os.makedirs(APP_DIR, exist_ok=True)

DATA_FILE = os.path.join(APP_DIR, "user_stats.json")
HISTORY_FILE = os.path.join(APP_DIR, "history_data.json")
DAILY_STREAK_DATA_FILE = os.path.join(APP_DIR, "daily_streak_data.json")

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"xp": 0, "level": 1, "total_tasks": 0}

def save_data(data):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving data: {e}")

user_stats = load_data()

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {"xp_history": {}, "tasks_history": {}}

def save_history(data):
    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

history_data = load_history()

def load_daily_streak_data():
    if os.path.exists(DAILY_STREAK_DATA_FILE):
        with open(DAILY_STREAK_DATA_FILE, "r") as f:
            return json.load(f)
    return {"consecutive_days": 0, "last_login": None}

def save_daily_login(data):
    with open(DAILY_STREAK_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

user_daily_login = load_daily_streak_data()

root = tk.Tk()
root.minsize(1000, 500)
root.title("Pomodoro App")

timer_on = False
study_duration = 60
timer = study_duration

is_break_time = False
break_duration = 60
break_timer = break_duration

pomodoro_open = False

distraction_punished = False

def start_studying_time(timer_label, pomodoro_popup):
    global timer_on
    if timer_on:
        return
    timer_on = True
    check_distractions()
    update_study_time(timer_label, pomodoro_popup)

def update_study_time(timer_label, pomodoro_popup):
    global timer_on, timer
    if timer_on and timer > 0:
        timer -= 1
        minutes = timer // 60
        seconds = timer % 60
        timer_label.config(text=f"Study time    {minutes}:{seconds:02d}")
        pomodoro_popup.after(1000, lambda: update_study_time(timer_label, pomodoro_popup))
    else:
        timer_on = False

def pause_studying_time():
    global timer_on
    timer_on = False

def reset_studying_time(timer_label):
    global timer, timer_on
    timer_on = False
    timer = study_duration
    minutes = timer // 60
    timer_label.config(text=f"Study time    {minutes}:00")

def start_break_time(break_label, pomodoro_popup):
    global is_break_time
    if is_break_time:
        return
    is_break_time = True
    update_break_time(break_label, pomodoro_popup)

def update_break_time(break_label, pomodoro_popup):
    global is_break_time, break_timer
    if is_break_time and break_timer > 0:
        break_timer -= 1
        minutes = break_timer // 60
        seconds = break_timer % 60
        break_label.config(text=f"Break time    {minutes}:{seconds:02d}")
        pomodoro_popup.after(1000, lambda: update_break_time(break_label, pomodoro_popup))
    else:
        is_break_time = False

def pause_break_time():
    global is_break_time
    is_break_time = False

def reset_break_time(break_label):
    global break_timer, is_break_time
    is_break_time = False
    break_timer = break_duration
    minutes = break_timer // 60
    break_label.config(text=f"Break time    {minutes}:00")

def pomodoro_window():
    global pomodoro_open, timer, break_timer
    pomodoro_open = True
    pomodoro_popup = tk.Toplevel(root)
    pomodoro_popup.title("Pomodoro Timer")
    pomodoro_popup.minsize(1000, 500)

    def on_close():
        global pomodoro_open, timer_on
        pomodoro_open = False
        timer_on = False
        pomodoro_popup.destroy()

    pomodoro_popup.protocol("WM_DELETE_WINDOW", on_close)

    input_frame = tk.Frame(pomodoro_popup)
    input_frame.pack(pady=40)

    tk.Label(input_frame, text="Study (min):", font=("Arial", 12)).grid(row=0, column=0)
    study_entry = tk.Entry(input_frame, width=5, font=("Arial", 12))
    study_entry.insert(0, "1")
    study_entry.grid(row=0, column=1)

    tk.Label(input_frame, text="Break (min):", font=("Arial", 12)).grid(row=0, column=2)
    break_entry = tk.Entry(input_frame, width=5, font=("Arial", 12))
    break_entry.insert(0, "1")
    break_entry.grid(row=0, column=3)

    def apply_times():
        global timer, break_timer, study_duration, break_duration
        try:
            study_mins = int(study_entry.get())
            break_mins = int(break_entry.get())
            timer = study_mins * 60
            break_timer = break_mins * 60
            study_duration = timer
            break_duration = break_timer
            timer_label.config(text=f"Study time    {study_mins}:00")
            break_label.config(text=f"Break time    {break_mins}:00")
        except ValueError:
            timer_label.config(text="Invalid input!")

    tk.Button(input_frame, text="Set Timers", command=apply_times).grid(row=0, column=4)

    timer_label = tk.Label(pomodoro_popup, text="Study time   1:00", font=("Helvetica", 24))
    timer_label.pack(pady=20)

    break_label = tk.Label(pomodoro_popup, text="Break time   1:00", font=("Helvetica", 24))
    break_label.pack(pady=20)

    tk.Button(pomodoro_popup, text="Start Studying", command=lambda: start_studying_time(timer_label, pomodoro_popup)).pack(side="left")
    tk.Button(pomodoro_popup, text="Pause Studying", command=pause_studying_time).pack(side="left")
    tk.Button(pomodoro_popup, text="Reset Studying Timer", command=lambda: reset_studying_time(timer_label)).pack(side="left")
    tk.Button(pomodoro_popup, text="Start Break", command=lambda: start_break_time(break_label, pomodoro_popup)).pack(side="left")
    tk.Button(pomodoro_popup, text="Pause Break", command=pause_break_time).pack(side="left")
    tk.Button(pomodoro_popup, text="Reset Break Timer", command=lambda: reset_break_time(break_label)).pack(side="left")

pomodoro_btn = tk.Button(root, text="Pomodoro", command=pomodoro_window)
pomodoro_btn.pack()

focus_label = tk.Label(root, text="")
focus_label.pack()

def focus_mode():
    root.attributes("-fullscreen", True)
    focus_label.config(text="FOCUS MODE IS ON - ESC TO EXIT", font=("Arial", 20))

def stop_focus_mode(event=None):
    root.attributes("-fullscreen", False)
    focus_label.config(text="")

root.bind("<Escape>", stop_focus_mode)

tk.Button(root, text="Focus", command=focus_mode).pack()

clock_display = tk.Label(root, text="", font=("Arial", 18))
clock_display.place(relx=1.0, rely=0.0, anchor="ne")

def get_current_time(clock_display):
    clock_display.config(text=datetime.datetime.now().strftime("%H:%M:%S"))
    root.after(1000, lambda: get_current_time(clock_display))

get_current_time(clock_display)

def add_task():
    global total_tasks, completed_tasks
    task_text = entry.get()
    if task_text.strip() == "":
        return

    total_tasks += 1
    update_progress()

    task_frame = tk.Frame(task_container, bg="lightgray")
    task_frame.pack(fill="x")

    completed = tk.BooleanVar()

    def on_check():
        global completed_tasks
        if completed.get():
            completed_tasks += 1
            add_xp(20)
        else:
            completed_tasks = max(0, completed_tasks - 1)
            add_xp(-20)
        update_progress()

    tk.Checkbutton(task_frame, variable=completed, command=on_check, bg="lightgray").pack(side="left")
    tk.Label(task_frame, text=task_text, bg="lightgray").pack(side="left")

    def on_delete():
        global total_tasks, completed_tasks
        total_tasks = max(0, total_tasks - 1)
        if completed.get():
            completed_tasks = max(0, completed_tasks - 1)
            add_xp(-20)
        task_frame.destroy()
        update_progress()

    tk.Button(task_frame, text="x", command=on_delete, fg="red").pack(side="right")

    entry.delete(0, tk.END)

top_frame = tk.Frame(root)
top_frame.pack()

entry = tk.Entry(top_frame)
entry.pack(side="left")

tk.Button(top_frame, text="Add Task", command=add_task).pack(side="left")

task_container = tk.Frame(root)
task_container.pack()

total_tasks = 0
completed_tasks = 0

progress_frame = tk.Frame(root)
progress_frame.pack()

progress_bar = ttk.Progressbar(progress_frame, length=400, mode="determinate")
progress_bar.pack()

progress_label = tk.Label(progress_frame, text="0 / 0 tasks completed")
progress_label.pack()

def update_progress():
    if total_tasks == 0:
        progress_bar["value"] = 0
        progress_label.config(text="0 / 0 tasks completed")
    else:
        progress_bar["maximum"] = total_tasks
        progress_bar["value"] = completed_tasks
        progress_label.config(text=f"{completed_tasks} / {total_tasks} tasks completed")

checkin_frame = tk.Frame(root)
checkin_frame.pack()

daily_log_in_streak_display = tk.Label(root, text=f"Log In Streak: {user_daily_login['consecutive_days']}")
daily_log_in_streak_display.pack()

def update_daily_log_in_ui():
    daily_log_in_streak_display.config(text=f"Log In Streak: {user_daily_login['consecutive_days']}")

def on_checkin():
    today = str(datetime.date.today())
    if user_daily_login["last_login"] == today:
        return
    user_daily_login["last_login"] = today
    user_daily_login["consecutive_days"] += 1
    save_daily_login(user_daily_login)
    update_daily_log_in_ui()
    checkin_frame.pack_forget()

tk.Checkbutton(checkin_frame, command=on_checkin).pack()

def add_xp(amount):
    global user_stats
    user_stats["xp"] += amount
    xp_needed = user_stats["level"] * 100
    if user_stats["xp"] >= xp_needed:
        user_stats["xp"] -= xp_needed
        user_stats["level"] += 1
    save_data(user_stats)

stats_frame = tk.Frame(root)
stats_frame.pack()

level_display = tk.Label(stats_frame, text=f"Level: {user_stats['level']}")
level_display.pack()

xp_display = tk.Label(stats_frame, text=f"XP: {user_stats['xp']}")
xp_display.pack()

def update_ui():
    level_display.config(text=f"Level: {user_stats['level']}")
    xp_display.config(text=f"XP: {user_stats['xp']}")

def check_distractions():
    global distraction_punished

    if not timer_on or not pomodoro_open:
        distraction_punished = False
        return

    active_window = gw.getActiveWindow()
    if active_window is None:
        return

    if "pomodoro" not in active_window.title.lower():
        if not distraction_punished:
            distraction_punished = True
            add_xp(-20)

            warning = tk.Toplevel(root)
            warning.title("DISTRACTION DETECTED")
            tk.Label(warning, text="-20 XP").pack()
            tk.Button(warning, text="OK", command=warning.destroy).pack()

def distraction_loop():
    check_distractions()
    root.after(3000, distraction_loop)

distraction_loop()

root.mainloop()