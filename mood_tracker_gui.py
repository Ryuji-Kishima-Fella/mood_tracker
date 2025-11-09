import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import csv, os

MOOD_FILE = "mood_log.txt"

class MoodTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mood Tracker v2.0")
        self.root.geometry("420x420")

        tk.Label(root, text="Select your mood:", font=("Arial", 14)).pack(pady=10)
        self.mood_var = tk.StringVar(value="😊 Happy")
        moods = ["😊 Happy", "😐 Neutral", "🤷 So-so", "😔 Sad", "😠 Angry", "😴 Tired"]
        self.option = tk.OptionMenu(root, self.mood_var, *moods)
        self.option.pack(pady=5)

        tk.Button(root, text="Log Mood", command=self.log_mood).pack(pady=10)
        tk.Button(root, text="View & Edit History", command=self.view_history).pack(pady=5)
        tk.Button(root, text="Export to CSV", command=self.export_csv).pack(pady=5)
        tk.Button(root, text="📊 View Summary", command=self.view_summary).pack(pady=5)

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

        win = tk.Toplevel(self.root)
        win.title("Mood History")
        win.geometry("400x400")

        # Scrollable listbox
        scrollbar = tk.Scrollbar(win)
        scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(win, selectmode=tk.SINGLE, yscrollcommand=scrollbar.set, font=("Consolas", 11))
        self.listbox.pack(expand=True, fill="both", padx=10, pady=10)
        scrollbar.config(command=self.listbox.yview)

        # Load entries
        self.entries = self.load_moods()
        for entry in self.entries:
            self.listbox.insert(tk.END, entry.strip())

        # Action buttons
        button_frame = tk.Frame(win)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="✏️ Edit", command=self.edit_entry).pack(side="left", padx=10)
        tk.Button(button_frame, text="❌ Delete", command=self.delete_entry).pack(side="left", padx=10)
        tk.Button(button_frame, text="🔄 Refresh", command=self.refresh_list).pack(side="left", padx=10)

    def load_moods(self):
        with open(MOOD_FILE, "r", encoding="utf-8") as f:
            return f.readlines()

    def refresh_list(self):
        # Reload the mood list after edit/delete
        self.listbox.delete(0, tk.END)
        self.entries = self.load_moods()
        for entry in self.entries:
            self.listbox.insert(tk.END, entry.strip())

    def edit_entry(self):
        # Edit the selected entry
        try:
            index = self.listbox.curselection()[0]
        except IndexError:
            messagebox.showwarning("Warning", "Please select an entry to edit.")
            return

        old_entry = self.entries[index].strip()
        new_mood = simpledialog.askstring("Edit Entry", f"Update mood for:\n{old_entry}", initialvalue=old_entry.split(" - ")[1])
        if new_mood:
            date = old_entry.split(" - ")[0]
            self.entries[index] =f"{date} - {new_mood}\n"
            self.save_all()
            self.refresh_list()
            messagebox.showinfo("Updated", "Mood entry updated successfully!")

    def delete_entry(self):
        # Delete the selected entry
        try:
            index = self.listbox.curselection()[0]
        except IndexError:
            messagebox.showwarning("warning", "Please select an entry to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this entry?")
        if confirm:
            del self.entries[index]
            self.save_all()
            self.refresh_list()
            messagebox.showinfo("Deleted", "Mood entry deleted successfully!")

    def save_all(self):
        # Rewrite all mood entries to the file
        with open(MOOD_FILE, "w", encoding="utf-8") as f:
            f.writelines(self.entries)

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

    def view_summary(self):
        # Display a pie chart summarizing mood frequencies.
        if not os.path.exists(MOOD_FILE):
            messagebox.showinfo("Summary", "No mood data available yet.")
            return

        # Count moods
        mood_counts = {}
        with open(MOOD_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if " - " in line:
                    _, mood = line.strip().split(" - ", 1)
                    mood_counts[mood] = mood_counts.get(mood, 0) + 1

        if not mood_counts:
            messagebox.showinfo("Summary", "No valid mood entries found.")
            return

        # Create new window for chart
        win = tk.Toplevel(self.root)
        win.title("Mood Summary")
        win.geometry("420x420")

        # Create matplotlib figure
        fig = Figure(figsize=(4, 4))
        ax = fig.add_subplot(111)
        moods = list(mood_counts.keys())
        counts = list(mood_counts.values())

        ax.pie(counts, labels=moods, autopct="%1.1f%%", startangle=90)
        ax.set_title("Mood Distribution")

        #Embed the figure in Tkinter 
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both")

        # Refresh button
        tk.Button(win, text="🔄 Refresh", command=lambda: [win.destroy(), self.view_summary()]).pack(pady=10)



if __name__ == "__main__":
    root = tk.Tk()
    app = MoodTrackerGUI(root)
    root.mainloop()
