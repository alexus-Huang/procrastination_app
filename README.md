# 🍅 Pomodoro Productivity App

An immersive, gamified desktop Pomodoro application built in Python using Tkinter. This application blends traditional time-management strategies with a dynamic RPG leveling framework, designed to incentivize deep focus and penalize off-task behavior.

---

## ✨ Features & Functionality

* **Customizable Timers:** Seamlessly set and apply your own personalized Study and Break durations via the input dashboard.
* **RPG Leveling Framework:** Stay motivated! Earn **+20 XP** for every task you complete on your to-do list and level up your profile as you climb the ranks.
* **Daily Streak Tracker:** Includes an integrated check-in mechanism that tracks and saves your consecutive daily login streaks to help you build lasting habits.
* **Interactive Statistics Portal:** View detailed, embedded analytical graphs (`matplotlib`) that track your lifetime XP gains and daily task completion history.
* **Anti-Distraction Enforcement:** The app monitors active system window titles during active study countdowns. If you switch to an unapproved tab or application, it triggers an instant warning dialogue and applies a **-20 XP penalty**.
* **Full-Screen Focus Mode:** Instantly expand the canvas into a borderless, distraction-free window constraint overlay to completely block out hardware display notifications (Press `ESC` to exit).

---

## 🧠 What I Learned

Developing this project provided hands-on experience with several core programming and software design concepts:

* **File I/O and JSON Data Handling:** Learned how to write, read, and save user state data cleanly to external `.json` files so progress persists even after the app closes.
* **OS Window Tracking (`pygetwindow`):** Discovered how to interact with the operating system to detect active window titles and create a functional anti-distraction system.
* **Data Visualization (`matplotlib`):** Learned how to generate and embed professional line graphs and bar charts into a custom statistics window UI.
* **Dynamic GUI States:** Mastered how to update text labels and UI countdown components dynamically in real time without lagging the main process.
* **Window Hierarchies (`tk.Toplevel`):** Gained an understanding of child windows, learning how to create secondary popups that naturally belong to the primary parent application (`root`).

---

## 🚀 How to Install and Run the App

Because this application relies on a virtual environment and system dependencies, you must properly extract the compressed project files before executing it.

### Step 1: Extract the Zip File
1. Locate your downloaded `procrastination_app-1.0.2.zip` file in your system **Downloads** folder.
2. **Right-click** on the zip file and select **Extract All...**
3. Click **Extract** on the window prompt. A brand-new, uncompressed folder window will automatically open up on your screen.

### Step 2: Open Command Prompt in the Project Folder
1. Press the **Windows Key** on your keyboard, type `cmd`, and press **Enter** to open the black Command Prompt terminal.
2. Type `cd ` (make sure to type a space after `cd`, but **do not** hit enter yet).
3. Go to your newly unzipped folder window from Step 1, click and hold its folder icon, then **drag and drop it directly into the black Command Prompt window**.
4. Press **Enter**. Your terminal prompt will now accurately display your project folder path.

### Step 3: Activate the Virtual Environment
To ensure the Python compiler can locate all the necessary visualization and window-hooking libraries, activate the isolated environment by running:
```cmd
.\venv\Scripts\activate