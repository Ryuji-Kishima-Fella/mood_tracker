import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import csv, os

MOOD_FILE = "mood_log.txt"

class MoodTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mood Tracker v2.0")
        self.root.geometry("400x400")

        tk.Label(root, text="Select your mood:", font=("Arial", 14)).pack(pady=10)
        self.mood_var = tk.StringVar(value="😊 Happy")
        moods = ["😊 Happy", "😐 Neutral", "🤷 So-so", "😔 Sad", "😠 Angry", "😴 Tired"]
        self.option = tk.OptionMenu(root, self.mood_var, *moods)
        self.option.pack(pady=5)

        tk.Button(root, text="Log Mood", command=self.log_mood).pack(pady=10)
        tk.Button(root, text="View History", command=self.view_history).pack(pady=5)
        tk.Button(root, text="Export to CSV", command=self.export_csv).pack(pady=5)

        self.status = tk.Label(root, text="", fg="gray")
        self.status.pack(side="bottom", fill="x", pady=5)

    def log_mood(self):
        mood = self.mood_var.get()
        with open(MOOD_FILE, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - {mood}\n")
        self.status.config(text=f"Mood saved: {mood}")
        messagebox.showinfo("Success", f"Mood '{mood}' logged!")

    def view_history(self):
        if not os.path.exists(MOOD_FILE):
            messagebox.showinfo("History", "No mood history yet.")
            return
        with open(MOOD_FILE, "r", encoding="utf-8") as f:
            history = f.read()
        win = tk.Toplevel(self.root)
        win.title("Mood History")
        text = tk.Text(win, wrap="word")
        text.insert("1.0", history)
        text.config(state="disabled")
        text.pack(expand=True, fill="both")

    ''' Delete function [Incomplete]
    def delete_history():
        if not os.path.exists(MOOD_FILE):
            messagebox.showinfo("Warning", "No mood history yet.")
            return
        with open(MOOD_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if not lines:
            messagebox.showinfo("⚠️ No entries to delete.")
            return
    '''


    def export_csv(self):
        if not os.path.exists(MOOD_FILE):
            messagebox.showwarning("Warning", "No mood data to export.")
            return
        with open(MOOD_FILE, "r", encoding="utf-8") as txt, open("mood_history.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Date", "Mood"])
            for line in txt:
                if " - " in line:
                    date, mood = line.strip().split(" - ", 1)
                    writer.writerow([date, mood])
        messagebox.showinfo("Export", "Mood history exported to CSV!")

if __name__ == "__main__":
    root = tk.Tk()
    app = MoodTrackerGUI(root)
    root.mainloop()
