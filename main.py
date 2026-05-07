import tkinter as tk
import math
root = tk.Tk()
root.minsize(1000,500)


timer_on = False
current_time = 1 * 60

break_time = False
break_time = 5 * 60

timer_label = tk.Label(root, text="25:00", font=("Helvetica",48))
timer_label.pack(pady=20)

break_label = tk.Label(root, text="5:00",font=("Helvetica",24))
break_label.pack(pady=20)

# pomodoro timer
def start_timer():
    global timer_on
    if not timer_on:
        count_down_timer(current_time)

def stop_timer():
    global timer_on
    if timer_on:
        root.after_cancel(timer_on)
        timer_on = False

def start_break():
    global break_time
    if not break_time:
        count_down_break(break_time)

def count_down_timer(count):
    global current_time, timer_on

    mins = count // 60
    secs = count % 60

    timer_label.config(text=f"{mins:02d}:{secs:02d}")

    if count > 0:
        current_sec = count
        timer_on = root.after(1000, count_down_timer, count - 1)
    else:
        timer_on = False
        print("Time's up!")

def count_down_break(count):
    pass

start_timer_btn = tk.Button(root,text="Start",command=start_timer,font=("Helvetica",24))
start_timer_btn.pack(pady=20)

stop_timer_btn = tk.Button(root,text="Stop",command=stop_timer,font=("Helvetica",24))
stop_timer_btn.pack(pady=10)
# task list

#daily streak system

#xp / leveling system

# statistics dashboard

#distraction punishment system

#focus mode

#animated UI
root.mainloop()