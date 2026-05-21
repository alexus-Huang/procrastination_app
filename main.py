import tkinter as tk
import math
import json
import os
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pygetwindow as gw
from tkinter import ttk

# user data
DATA_FILE = "save_data.json"
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"xp":0, "level":1,"total_tasks":0}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data,f,indent=4)

user_stats = load_data()

# Historical Data ( for stats )
HISTORY_FILE = "history_data.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {"xp_history": {}, "tasks_history": {}}

def save_history(data):
    with open(HISTORY_FILE,"w") as f:
        json.dump(data,f,indent=4)

history_data = load_history()

# Daily Streak System
DAILY_STREAK_DATA_FILE = "daily_streak_data.json"
def load_daily_streak_data():
    if os.path.exists(DAILY_STREAK_DATA_FILE):
        with open(DAILY_STREAK_DATA_FILE, "r") as daily_streak_file:
            return json.load(daily_streak_file)
    return {"consecutive_days": 0, "last_login": None}

def save_daily_login(data):
    with open(DAILY_STREAK_DATA_FILE, "w") as daily_streak_file:
        json.dump(data, daily_streak_file, indent=4)

user_daily_login = load_daily_streak_data()
root = tk.Tk()
root.minsize(1000,500)

# popup windows
#pomodoro timer
timer_on = False
study_duration = 1 * 60

is_break_time = False
break_duration = 1 * 60

pomodoro_open = False
#studying functions
def start_studying_time(timer_label,pomodoro_popup):
    global timer_on
    if timer_on:
        return
    timer_on = True
    check_distractions()
    update_study_time(timer_label,pomodoro_popup)

def update_study_time(timer_label,pomodoro_popup):
    global timer_on, timer
    if timer_on and timer > 0:
        timer -=1
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
    timer = study_duration   # reset to original set duration
    minutes = timer // 60
    timer_label.config(text=f"Study time    {minutes}:{00:02d}")

#break functions
def start_break_time(break_label,pomodoro_popup):
    global is_break_time
    if is_break_time:
        return
    is_break_time = True
    update_break_time(break_label,pomodoro_popup)

def update_break_time(break_label,pomodoro_popup):
    global is_break_time, break_timer
    if is_break_time and break_timer > 0:
        break_timer-=1
        minutes = break_timer // 60
        seconds = break_timer % 60
        break_label.config(text=f"Break time    {minutes}:{seconds:02d}")
        pomodoro_popup.after(1000,lambda: update_break_time(break_label, pomodoro_popup))
    else:
        is_break_time = False

def pause_break_time():
    global is_break_time
    is_break_time = False

def reset_break_time(break_label):
    global break_timer, is_break_time
    is_break_time = False
    break_timer = break_duration   # reset to original set duration
    minutes = break_timer // 60
    break_label.config(text=f"Break time    {minutes}:{00:02d}")

def pomodoro_window():
    global pomodoro_open, timer, break_timer
    pomodoro_open = True
    pomodoro_popup = tk.Toplevel(root)
    pomodoro_popup.title("Pomodoro Timer")
    pomodoro_popup.minsize(1000,500)

    def on_close():
        global pomodoro_open, timer_on
        pomodoro_open = False
        timer_on = False
        pomodoro_popup.destroy()
    
    pomodoro_popup.protocol("WM_DELETE_WINDOW", on_close)

    # Timer input fields
    input_frame = tk.Frame(pomodoro_popup)
    input_frame.pack(pady=40)

    tk.Label(input_frame,text="Study (min):", font=("Arial",12)).grid(row=0, column=2, padx=5)
    study_entry = tk.Entry(input_frame, width=5, font=("Arial",12))
    study_entry.insert(0,"1") # default 1 min
    study_entry.grid(row=0, column=1, padx=5)

    tk.Label(input_frame,text="Break (min):", font=("Arial",12)).grid(row=0, column=2, padx=5)
    break_entry = tk.Entry(input_frame, width=5, font=("Arial",12))
    break_entry.insert(0,"1") # default 1 min
    break_entry.grid(row=0, column=3, padx=5)

    def apply_times():
        global timer, break_timer, timer_on, is_break_time, study_duration, break_duration
        timer_on = False
        is_break_time = False
        try:
            study_mins = int(study_entry.get())
            break_mins = int(break_entry.get())
            timer = study_mins * 60
            break_timer = break_mins * 60
            study_duration = timer       # save originals
            break_duration = break_timer
            timer_label.config(text=f"Study time    {study_mins}:{00:02d}")
            break_label.config(text=f"Break time    {break_mins}:{00:02d}")
        except ValueError:
            timer_label.config(text="Invalid input!")
    
    apply_btn = tk.Button(input_frame, text="Set Timers", command=apply_times, font=("Arial", 12))
    apply_btn.grid(row=0, column=4, padx=10)

    #labels
    timer_label = tk.Label(pomodoro_popup,text="Study time   1:00",font=("Helvetica",24))
    timer_label.pack(pady=20)

    break_label = tk.Label(pomodoro_popup,text="Break time   1:00",font=("Helvetica",24))
    break_label.pack(pady=20)

    #buttons
    start__studying_timer = tk.Button(pomodoro_popup,text="Start Studying",command= lambda: start_studying_time(timer_label,pomodoro_popup))
    start__studying_timer.pack(side="left",padx=5)

    pause_studying_timer = tk.Button(pomodoro_popup,text="Pause Studying",command=pause_studying_time)
    pause_studying_timer.pack(side="left",padx=5)

    reset_studying_timer = tk.Button(pomodoro_popup,text="Reset Studying Timer",command= lambda: reset_studying_time(timer_label))
    reset_studying_timer.pack(side="left",padx=5)

    start_break_timer = tk.Button(pomodoro_popup, text="Start Break",command= lambda: start_break_time(break_label,pomodoro_popup))
    start_break_timer.pack(side="left",padx=5)

    pause_break_timer = tk.Button(pomodoro_popup, text="Pause Break", command=pause_break_time)
    pause_break_timer.pack(side="left",padx=5)

    reset_break_timer = tk.Button(pomodoro_popup,text="Reset Break Timer",command= lambda: reset_break_time(break_label))
    reset_break_timer.pack(side="left",padx=5)

pomodoro_btn = tk.Button(root, text="Pomodoro",command=pomodoro_window)
pomodoro_btn.pack()

#focus mode
focus_label = tk.Label(root,text="")
focus_label.pack(padx=5,pady=5)
def focus_mode():
    root.attributes("-fullscreen",True)
    focus_label.config(text="FOCUS MODE IS ON - ESC TO EXIT",font=("Arial",20))

def stop_focus_mode(event=None):
    root.attributes("-fullscreen",False)
    focus_label.config(text="")
root.bind("<Escape>",stop_focus_mode)

focus_btn = tk.Button(root, text="Focus",font=("Arial",20),command=focus_mode)
focus_btn.pack(padx=5)

# main page 

# clock
clock_display = tk.Label(root,text="",font=("Arial",18))
clock_display.place(relx=1.0,rely=0.0, anchor="ne")

def get_current_time(clock_display):
    current_time = datetime.datetime.now()
    str_current_time = current_time.strftime("%H:%M:%S")
    clock_display.config(text=str_current_time)
    root.after(1000,lambda:get_current_time(clock_display))

get_current_time(clock_display)
# task list
def add_task():
    task_text = entry.get()
    if task_text.strip() == "":
        return

    # update total_tasks
    global total_tasks
    total_tasks += 1
    update_progress()
    task_frame = tk.Frame(task_container, bg="lightgray",pady=5)
    task_frame.pack(fill="x",padx=10,pady=5)

    def on_check():
        global completed_tasks, total_tasks
        if completed.get():
            completed_tasks += 1
            add_xp(20)
            task_label.config(fg="gray")
            today = str(datetime.date.today())
            history_data["tasks_history"][today] = history_data["tasks_history"].get(today,0) + 1
            save_history(history_data)
        else:
            completed_tasks -= 1
            add_xp(-20)
            task_label.config(fg="black")
            save_data(user_stats)
            update_ui()
        
        update_progress()

    completed = tk.BooleanVar()
    checkbox = tk.Checkbutton(
        task_frame,
        variable=completed,
        bg="lightgray",
        command=on_check
    )
    checkbox.pack(side="left",padx=5)

    task_label = tk.Label(
        task_frame,
        text=task_text,
        bg="lightgray",
        font=("Arial",14),
        anchor="w"
    )
    task_label.pack(side="left",padx=10)

    def on_delete():
        global total_tasks, completed_tasks
        total_tasks -= 1
        if completed.get():
            completed_tasks -= 1    
            add_xp(-20)
        task_frame.destroy()
        update_progress()
    
    delete_button = tk.Button(
        task_frame,
        text="x",
        fg="red",
        command=on_delete
    )
    delete_button.pack(side="right",padx=10)
    entry.delete(0,tk.END)

top_frame = tk.Frame(root)
top_frame.pack(pady=20)

entry = tk.Entry(top_frame,width=25,font=("Arial",14))
entry.pack(side="left",padx=5)

add_button = tk.Button(
    top_frame,
    text="Add Task",
    command=add_task
)
add_button.pack(side="left")

task_container = tk.Frame(root)
task_container.pack(fill="both",expand=True)
total_tasks = 0
completed_tasks = 0

# Progress bar
progress_frame = tk.Frame(root)
progress_frame.pack(fill="x", padx=20, pady=10)

progress_bar = ttk.Progressbar(progress_frame, length = 400, mode="determinate")
progress_bar.pack(fill="x")

progress_label = tk.Label(progress_frame, text="0 / 0 tasks completed",fg="gray", font=("Arial",11))
progress_label.pack()

def update_progress():
    if total_tasks == 0:
        progress_bar['value'] = 0
        progress_label.config(text="0 / 0 tasks completed")
    else:
        progress_bar["maximum"] = total_tasks
        progress_bar["value"] = completed_tasks
        progress_label.config(text=f"{completed_tasks} / {total_tasks} tasks completed")
#daily streak system
checkin_frame = tk.Frame(root)
checkin_frame.pack(pady=5)

def add_days(logged_in):
    global user_daily_login
    user_daily_login["consecutive_days"] += logged_in
    save_daily_login(user_daily_login)
    update_daily_log_in_ui()

daily_log_in_frame = tk.Frame(root)
daily_log_in_frame.pack(pady=10)

daily_log_in_streak_display = tk.Label(daily_log_in_frame, text=f"Log In Streak: {user_daily_login['consecutive_days']}",font=("Arial",14,"bold"))
daily_log_in_streak_display.pack(side="left",padx=20)

def update_daily_log_in_ui():
    daily_log_in_streak_display.config(text=f"Log In Streak: {user_daily_login['consecutive_days']}")

def check_streak():
    today_date = str(datetime.date.today())
    last = user_daily_login.get("last_login")
    if today_date == last:
        checkin_frame.pack_forget()
    elif last == str(datetime.date.today() - datetime.timedelta(days=1)):
        pass
    else:
        user_daily_login["consecutive_days"] = 0

def on_checkin():
    today = str(datetime.date.today())
    if user_daily_login["last_login"] == today:
        return
    user_daily_login["last_login"] = today
    user_daily_login["consecutive_days"] += 1
    save_daily_login(user_daily_login)
    update_daily_log_in_ui()
    checkin_frame.pack_forget()

checkin_var = tk.BooleanVar()
checkin_checkbox = tk.Checkbutton(
    checkin_frame,
    variable=checkin_var,
    command=on_checkin
)
checkin_checkbox.pack()
check_streak()

# XP / Leveling System
def add_xp(amount):
    global user_stats
    user_stats["xp"] += amount
    xp_needed = user_stats["level"] * 100
    if user_stats["xp"] >= xp_needed:
        user_stats["xp"] -= xp_needed
        user_stats["level"] += 1
        print(f"Level Up! Now level {user_stats['level']}")
    save_data(user_stats)
    update_ui()
    today = str(datetime.date.today())
    if amount > 0:
        history_data["xp_history"][today] = history_data["xp_history"].get(today,0) + amount
        save_history(history_data)

stats_frame = tk.Frame(root)
stats_frame.pack(pady=10)

level_display = tk.Label(stats_frame,text=f"Level: {user_stats['level']}",font=("Arial",14,"bold"))
level_display.pack(side="left",padx=20)

xp_display = tk.Label(stats_frame,text=f"XP: {user_stats['xp']} / {user_stats['level'] * 100}", font=("Arial",12))
xp_display.pack(side="left")

def update_ui():
    level_display.config(text=f"Level: {user_stats['level']}")
    xp_display.config(text=f"XP: {user_stats['xp']} / {user_stats['level'] * 100}")

# statistics dashboard
def statistics_popup():

    stats_window = tk.Toplevel(root)
    stats_window.title("Statistics")
    stats_window.minsize(1000, 600)

    fig, (ax1,ax2,ax3) = plt.subplots(1, 3, figsize=(14,4))
    fig.tight_layout(pad=4.0)

    # XP Data
    xp_data = history_data["xp_history"]
    if xp_data:
        dates = list(xp_data.keys())
        xp_values = list(xp_data.values())
        ax1.plot(dates,xp_values,marker="o",color="blue")
        ax1.set_title("XP Earned Over Time")
        ax1.set_xlabel("Date")
        ax1.set_ylabel("XP")
        ax1.tick_params(axis="x", rotation=45)
    else:
        ax1.text(0.5, 0.5, "No data yet", ha="center", va="center")
        ax1.set_title("XP Earned Over Time")

    # Tasks completed per day
    tasks_data = history_data["tasks_history"]
    if tasks_data:
        dates = list(tasks_data.keys())
        task_values = list(tasks_data.values())
        ax2.bar(dates, task_values, color="green")
        ax2.set_title("Tasks Completed Per Day")
        ax2.set_xlabel("Date")
        ax2.set_ylabel("Tasks")
        ax2.tick_params(axis="x", rotation=45)
    else:
        ax2.text(0.5, 0.5, "No data yet", ha="center", va="center")
        ax2.set_title("Tasks Completed Per Day")

    # Login streak
    ax3.plot(["Current Streak"], [user_daily_login["consecutive_days"]], marker="o", color="orange")
    ax3.set_title("Login Streak")
    ax3.set_ylabel("Days")

    # embed in tkinter
    canvas = FigureCanvasTkAgg(fig, master=stats_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

statistics_btn = tk.Button(root,text="Stats",font=("Helvetica",14),command=statistics_popup)
statistics_btn.pack(side="right",padx=5)

#distraction punishment system - in the background
distraction_punished = False

def check_distractions():
    global distraction_punished

    if not timer_on or not pomodoro_open:
        distraction_punished = False
        return
    
    allowed_titles = [root.title().lower(),"pomodoro timer"]
    active_window = gw.getActiveWindow() # Gets the user's current window
    print(active_window.title)
    if active_window is not None:
        if not any(t in active_window.title.lower() for t in allowed_titles):
            if not distraction_punished:
                distraction_punished = True
                add_xp(-20)

                #popup warning to the user
                warning = tk.Toplevel(root)
                warning.title("DISTRACTION DETECTED")
                tk.Label(warning,text="You switched away during study time!\n-20 XP",font=("Helvetica",18)).pack(pady=20)
                tk.Button(warning,text="OK",command=warning.destroy).pack(pady=10)
        else:
            distraction_punished = False # switched back, reset punishment system function
    
    root.after(3000,check_distractions)
    
def streak_damage():
    add_xp(-15)   

root.mainloop()