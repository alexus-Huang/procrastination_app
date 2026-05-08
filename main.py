import tkinter as tk
import math
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
        
def stop_studying_time():
    global timer_on
    timer_on = False


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

def stop_break_time():
    global is_break_time
    is_break_time = False

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
    start_timer = tk.Button(pomodoro_popup,text="Start Studying",command= lambda: start_studying_time(timer_label,pomodoro_popup))
    start_timer.pack(side="left",padx=5)

    stop_timer = tk.Button(pomodoro_popup,text="Stop Studying",command=stop_studying_time)
    stop_timer.pack(side="left",padx=5)

    start_break = tk.Button(pomodoro_popup, text="Start Break",command= lambda: start_break_time(break_label,pomodoro_popup))
    start_break.pack(side="left",padx=5)

    stop_break = tk.Button(pomodoro_popup, text="Stop Break", command=stop_break_time)
    stop_break.pack(side="left",padx=5)

pomodoro_btn = tk.Button(root, text="Pomodoro",command=pomodoro_window)
pomodoro_btn.pack()


#focus mode



# main page 

# task list

#daily streak system

#xp / leveling system

# statistics dashboard

# background
#distraction punishment system
#animated UI
root.mainloop()