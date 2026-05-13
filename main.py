import tkinter as tk
import math
import json
import os
import datetime
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
timer = 1 * 60

is_break_time = False
break_timer = 1 * 60

#studying functions
def start_studying_time(timer_label,pomodoro_popup):
    global timer_on
    if timer_on:
        return
    timer_on = True
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
    global timer
    timer = 1 * 60
    timer_label.config(text="Study time    1:00")

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
    global break_timer
    break_timer = 1 * 60
    break_label.config(text="Break time    1:00")

def pomodoro_window():
    pomodoro_popup = tk.Toplevel(root)
    pomodoro_popup.title("Pomodoro Timer")
    pomodoro_popup.minsize(1000,500)

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

def stop_focus_mode(event=None  ):
    root.attributes("-fullscreen",False)
    focus_label.config(text="")
root.bind("<Escape>",stop_focus_mode)

focus_btn = tk.Button(root, text="Focus",font=("Arial",20),command=focus_mode)
focus_btn.pack(padx=5)

# main page 
# task list
def add_task():
    task_text = entry.get() # get user's text
    if task_text.strip() == "":
        return
    task_frame = tk.Frame(task_container, bg="lightgray",pady=5)
    task_frame.pack(fill="x",padx=10,pady=5)

    def on_check():
        if completed.get():
            add_xp(20)
            task_label.config(fg="gray")
        else:
            add_xp(-20)
            task_label.config(fg="black")
            save_data(user_stats)
            update_ui()

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

    delete_button = tk.Button(
        task_frame,
        text="x",
        fg="red",
        command=task_frame.destroy
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

#daily streak system
checkin_frame = tk.Frame(root)
checkin_frame.pack(pady=5)

def add_days(logged_in):
    global user_daily_login
    user_daily_login["consecutive_days"] += logged_in # when the user checks the checkbox, update days
    save_daily_login(user_daily_login)
    update_daily_log_in_ui()

daily_log_in_frame = tk.Frame(root)
daily_log_in_frame.pack(pady=10)

daily_log_in_streak_display = tk.Label(daily_log_in_frame, text=f"Log In Streak: {user_daily_login["consecutive_days"]}",font=("Arial",14,"bold"))
daily_log_in_streak_display.pack(side="left",padx=20)

def update_daily_log_in_ui():
    daily_log_in_streak_display.config(text=f"Log In Streak: {user_daily_login["consecutive_days"]}")

def check_streak():
    today_date = str(datetime.date.today())
    last = user_daily_login.get("last_login")

    if today_date == last:
        checkin_frame.pack_forget()
    elif last == str(datetime.date.today() - datetime.timedelta(days=1)):
        pass # show checkbox since streak is still going
    else:
        user_daily_login["consecutive_days"] = 0 # user missed a day, reset streak

def on_checkin():
    user_daily_login["last_login"] = str(datetime.date.today())
    user_daily_login["consecutive_days"] +=1
    save_daily_login(user_daily_login)
    update_daily_log_in_ui()
    checkin_frame.pack_forget() # hide checkbox after log in

checkin_var = tk.BooleanVar()
checkin_checkbox = tk.Checkbutton(
    checkin_frame,
    variable=checkin_var,
    command=on_checkin
)
checkin_checkbox.pack()

# XP / Leveling System
def add_xp(amount):
    global user_stats
    user_stats["xp"] += amount

    xp_needed = user_stats["level"] * 100

    if user_stats["xp"] >= xp_needed:
        user_stats["xp"] -= xp_needed
        user_stats["level"] +=1
        print(f"Level Up! Now level {user_stats["level"]}")
    save_data(user_stats)
    update_ui()

stats_frame = tk.Frame(root)
stats_frame.pack(pady=10)

level_display = tk.Label(stats_frame,text=f"Level: {user_stats["level"]}",font=("Arial",14,"bold"))
level_display.pack(side="left",padx=20)

xp_display = tk.Label(stats_frame,text=f"XP: {user_stats["xp"]} / {user_stats["level"] * 100}", font=("Arial",12))
xp_display.pack(side="left")

def update_ui():
    level_display.config(text=f"Level: {user_stats["level"]}")
    xp_display.config(text=f"XP: {user_stats["xp"]} / {user_stats["level"] * 100}")

# statistics dashboard
def statistics_popup():
    print("stats popup window")

statistics_btn = tk.Button(root,text="Stats",font=("Helvetica",14),command=statistics_popup)
statistics_btn.pack(side="right",padx=5)
# background
#distraction punishment system

#animated UI
root.mainloop()