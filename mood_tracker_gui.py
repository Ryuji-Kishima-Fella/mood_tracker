import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import csv, os

MOOD_FILE = "mood_log.txt"
MOODS = ["😊 Happy", "😐 Neutral", "🤷 Bored", "😔 Sad", "😠 Angry", "😴 Tired"]

class MoodTrackerGUI:
    def __init__(self, root):
        # Theme configuration
        ctk.set_appearance_mode("dark")       # or "system" for auto mode
        ctk.set_default_color_theme("blue")

        self.root = root
        self.root.title("Mood Tracker v2.1")
        self.root.geometry("520x560")

        # --- Header ---
        ctk.CTkLabel(self.root, text="Select your mood:", font=("Arial", 16, "bold")).pack(pady=(20, 10))
        self.mood_var = ctk.StringVar(value=MOODS[0])
        self.option = ctk.CTkOptionMenu(self.root, values=MOODS, variable=self.mood_var)
        self.option.pack(pady=(0, 15))

        # --- Buttons ---
        btn_frame = ctk.CTkFrame(self.root)
        btn_frame.pack(padx=12, pady=(0, 15), fill="x")
        ctk.CTkButton(btn_frame, text="📝 Log Mood", command=self.log_mood).pack(side="left", padx=8, pady=8)
        ctk.CTkButton(btn_frame, text="📜 History", command=self.view_history).pack(side="left", padx=8, pady=8)
        ctk.CTkButton(btn_frame, text="💾 Export CSV", command=self.export_csv).pack(side="left", padx=8, pady=8)

        ctk.CTkButton(self.root, text="📊 View Summary", command=self.view_summary).pack(pady=(0, 8))
        ctk.CTkButton(self.root, text="🌓 Toggle Theme", command=self.toggle_theme).pack(pady=(0, 8))

        # --- Status Bar ---
        self.status = ctk.CTkLabel(
            self.root,
            text="Ready",
            text_color=("gray10", "gray80"),
            fg_color=("gray85", "gray20"),
            corner_radius=5
        )
        self.status.pack(side="bottom", fill="x", padx=8, pady=8)

        # --- State ---
        self.summary_window = None
        self.history_window = None
        self.entries = []

        # Create file if missing
        if not os.path.exists(MOOD_FILE):
            open(MOOD_FILE, "a", encoding="utf-8").close()

    # -----------------------------------------------------------
    # Utility
    # -----------------------------------------------------------
    def load_moods(self):
        with open(MOOD_FILE, "r", encoding="utf-8") as f:
            return f.readlines()

    def save_all(self):
        with open(MOOD_FILE, "w", encoding="utf-8") as f:
            f.writelines(self.entries)

    # -----------------------------------------------------------
    # Core Features
    # -----------------------------------------------------------
    def log_mood(self):
        mood = self.mood_var.get()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(MOOD_FILE, "a", encoding="utf-8") as f:
            f.write(f"{timestamp} - {mood}\n")
        self.status.configure(text=f"Mood saved: {mood}")
        messagebox.showinfo("Success", f"Mood '{mood}' logged!")

        if self.history_window and self.history_window.winfo_exists():
            self.populate_history()

        if self.summary_window and self.summary_window.winfo_exists():
            self.render_summary_chart(self.summary_window)

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
        messagebox.showinfo("Export", "Mood history exported successfully!")

    # -----------------------------------------------------------
    # History View
    # -----------------------------------------------------------
    def view_history(self):
        if self.history_window and self.history_window.winfo_exists():
            self.history_window.lift()
            self.history_window.focus_force()
            return

        win = ctk.CTkToplevel(self.root)
        win.title("Mood History")
        win.geometry("460x500")
        self.history_window = win

        # Bring it to the front
        win.lift()
        win.focus_force()
        win.attributes("-topmost", True)
        win.after(500, lambda: win.attributes("-topmost", False)) # avoid permanent always-on-top

        ctk.CTkLabel(win, text="Mood History", font=("Arial", 16, "bold")).pack(pady=10)

        # Fitler Dropdown
        filter_frame = ctk.CTkFrame(win)
        filter_frame.pack(pady=5)
        ctk.CTkLabel(filter_frame, text="Filter: ").pack(side="left", padx=5)

        self.history_filter = ctk.StringVar(value="All")
        dropdown = ctk.CTkOptionMenu(
            filter_frame,
            values=["All", "Today", "Last 7 Days", "Last 30 Days"],
            variable=self.history_filter,
            command=lambda _: self.populate_history()
        )
        dropdown.pack(side="left")

        # Scrollable Frame for entries
        self.history_frame = ctk.CTkScrollableFrame(win, width=420, height=360)
        self.history_frame.pack(padx=10, pady=5, fill="both", expand=True)

        # Populate entries dynamically
        self.populate_history()

    def filter_moods_by_date(self, entries, mode="All"):
        # Return filtered mood entries based on the selected time range.
        if mode == "All":
            return entries
        
        now = datetime.now()
        filtered = []

        for line in entries:
            if " - " not in line:
                continue
            date_str, mood = line.strip().split(" - ", 1)
            try:
                entry_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue

            if mode == "Today" and entry_date.date() == now.date():
                filtered.append(line)
            elif mode == "Last 7 Days" and (now - entry_date).days <= 7:
                filtered.append(line)
            elif mode == "Last 30 Days" and (now - entry_date).days <= 30:
                filtered.append(line)

        return filtered

    def populate_history(self):
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        all_entries = self.load_moods()
        filter_mode = self.history_filter.get() if hasattr(self, "history_fitler") else "All"
        self.entries = self.filter_moods_by_date(all_entries, filter_mode)

        if not self.entries:
            ctk.CTkLabel(self.history_frame, text="No entries yet.", text_color="gray").pack(pady=10)
            return

        for idx, entry in enumerate(self.entries):
            row = ctk.CTkFrame(self.history_frame)
            row.pack(fill="x", padx=6, pady=4)

            ctk.CTkLabel(row, text=entry.strip(), anchor="w", justify="left").pack(side="left", padx=5, pady=4)

            edit_btn = ctk.CTkButton(row, text="✏️", width=28, command=lambda i=idx: self.edit_entry(i))
            edit_btn.pack(side="right", padx=2)
            del_btn = ctk.CTkButton(row, text="❌", width=28, command=lambda i=idx: self.delete_entry(i))
            del_btn.pack(side="right", padx=2)

    # -----------------------------------------------------------
    # Edit/Delete
    # -----------------------------------------------------------
    def edit_entry(self, idx):
        old_entry = self.entries[idx].strip()
        date, old_mood = old_entry.split(" - ", 1)

        edit_win = ctk.CTkToplevel(self.root)
        edit_win.title("Edit Mood Entry")
        edit_win.geometry("320x160")

        ctk.CTkLabel(edit_win, text=f"Date: {date}", anchor="w").pack(pady=(10, 5))
        ctk.CTkLabel(edit_win, text="Select new mood:").pack(pady=(0, 6))

        mood_var = ctk.StringVar(value=old_mood)
        dropdown = ctk.CTkOptionMenu(edit_win, values=MOODS, variable=mood_var)
        dropdown.pack(pady=(0, 10))

        def save_edit():
            new_mood = mood_var.get()
            self.entries[idx] = f"{date} - {new_mood}\n"
            self.save_all()
            self.populate_history()
            messagebox.showinfo("Updated", f"Updated mood to '{new_mood}'")
            edit_win.destroy()

            if self.summary_window and self.summary_window.winfo_exists():
                self.render_summary_chart(self.summary_window)

        ctk.CTkButton(edit_win, text="💾 Save", command=save_edit).pack(pady=5)
        ctk.CTkButton(edit_win, text="❌ Cancel", command=edit_win.destroy).pack(pady=5)

    def delete_entry(self, idx):
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this entry?")
        if not confirm:
            return

        del self.entries[idx]
        self.save_all()
        self.populate_history()
        messagebox.showinfo("Deleted", "Mood entry deleted successfully!")

        if self.summary_window and self.summary_window.winfo_exists():
            self.render_summary_chart(self.summary_window)

    # -----------------------------------------------------------
    # Summary Chart
    # -----------------------------------------------------------
    def view_summary(self):
        if self.summary_window and self.summary_window.winfo_exists():
            self.summary_window.lift()
            self.summary_window.focus_force()
            return

        win = ctk.CTkToplevel(self.root)
        win.title("Mood Summary")
        win.geometry("480x480")

        # Bring it to the front
        win.lift()
        win.focus_force()
        win.attributes("-topmost", True)
        win.after(500, lambda: win.attributes("-topmost", False)) 

        self.summary_window = win
        self.render_summary_chart(win)

    def render_summary_chart(self, win):
        # Clear and re-render chart based on date filter
        for widget in win.winfo_children():
            widget.destroy()

        # Filter section
        filter_frame = ctk.CTkFrame(win)
        filter_frame.pack(pady=5)
        ctk.CTkLabel(filter_frame, text="Filter: ").pack(side="left", padx=5)

        filter_var = ctk.StringVar(value=getattr(self, "summary_filter", "All"))
        dropdown = ctk.CTkOptionMenu(
            filter_frame,
            values=["All", "Today", "Last 7 Days", "Last 30 Days"],
            variable=filter_var,
            command=lambda _: self.update_summary_filter(filter_var.get())
        )
        dropdown.pack(side="left")

        # Filtered data
        all_entries = self.load_moods()
        filtered_entries = self.filter_moods_by_date(all_entries, filter_var.get())

        mood_counts = {}
        for line in filtered_entries:
            if " - " in line:
                _, mood = line.strip().split(" - ", 1)
                mood_counts[mood] = mood_counts.get(mood, 0) + 1

        if not mood_counts:
            ctk.CTkLabel(win, text="No data for selected data.", text_color="gray").pack(pady=20)
            return

        current_mode = ctk.get_appearance_mode().lower()
        bg_color = "#242424" if current_mode == "dark" else "#ffffff"
        text_color = "white" if current_mode == "dark" else "black"

        fig = Figure(figsize=(5, 4), facecolor=bg_color)
        ax = fig.add_subplot(111, facecolor=bg_color)
        moods = list(mood_counts.keys())
        counts = list(mood_counts.values())

        wedges, texts, autotexts = ax.pie(
            counts,
            labels=moods,
            autopct="%1.1f%%",
            startangle=90,
            textprops={"color": text_color}
        )
        ax.set_title("Mood Distribution", color=text_color)
        ax.axis("equal")

        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both", padx=8, pady=8)

        ctk.CTkButton(win, text="🔄 Refresh", command=lambda: self.render_summary_chart(win)).pack(pady=8)

    def update_summary_filter(self, value):
        self.summary_filter = value
        if self.summary_window and self.summary_window.winfo_exists():
            self.render_summary_chart(self.summary_window)

    # -----------------------------------------------------------
    # Theme Toggle
    # -----------------------------------------------------------
    def toggle_theme(self):
        current = ctk.get_appearance_mode()
        new_mode = "light" if current == "dark" else "dark"
        ctk.set_appearance_mode(new_mode)
        self.status.configure(text=f"Switched to {new_mode} mode")

        if self.summary_window and self.summary_window.winfo_exists():
            self.render_summary_chart(self.summary_window)
        if self.history_window and self.history_window.winfo_exists():
            self.populate_history()


# -----------------------------------------------------------
# App Entry
# -----------------------------------------------------------
if __name__ == "__main__":
    root = ctk.CTk()
    app = MoodTrackerGUI(root)
    root.mainloop()
