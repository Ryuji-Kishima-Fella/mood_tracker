![Python](https://img.shields.io/badge/python-3.14-blue)
![GitHub last commit](https://img.shields.io/github/last-commit/Ryuji-Kishima-Fella/mood_tracker)
![License](https://img.shields.io/badge/license-MIT-green)


![Mood Tracker Screenshot](assets/mood_tracker_screenshot.png)

# Mood Tracker (Python)
> ![Version](https://img.shields.io/github/v/tag/Ryuji-Kishima-Fella/mood_tracker?sort=semver)
![Status](https://img.shields.io/badge/status-active-success)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/Ryuji-Kishima-Fella/mood_tracker?style=for-the-badge&color=blue)


A simple Python program that helps you record, view, and analyze your daily moods - created as part of my journey learning Python and GitHub version control. 

---

## 🚀 Current Version: v2.3

### What’s New in v2.3
- ⌨️ Keyboard shortcuts for faster navigation
- 🪟 Improved popup window handling (Escape to close active windows)
- 🧠 Better internal state management for GUI windows
- 🛠 Overall UX polish and stability improvements

---


## 🌟 Features

- 📝 **Log your mood** for the day  
- 📖 **View your mood history** (stored in a local text file)  
- 📊 **See a mood summary** showing how often each mood occurs  
- 📤 **Export mood history to CSV** for data analysis (NEW!)  
- 💾 All data saved locally for privacy and simplicity  

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|--------|-------|
| Ctrl + L | Log mood |
| Ctrl + H | Open mood history |
| Ctrl + S | Open mood summary |
| Ctrl + E | Export moods to CSV |
| Ctrl + T | Toggle dark/light mode |
| Esc | Close active window |
| Alt + F4 | Exit application |


---

## About the Project
The Mood Tracker started as a console-based learning project to practice:
- File I/O in Python
- Simple analytics (frequency counting)
- Structured program flow
- Git and GitHub fundamentals

From **v2.0 onward**, the project transitioned to a **GUI-based desktop application**, introducing:
- Event-driven programming
- Window lifecycle management
- Data visualization with Matplotlib
- Keyboard accessibility and UX improvements

This project reflects **incremental learning and continuous refinement**, rather than a one-off assignment.


---

## How to Run
1. Install Python 3.10+
2. Download or clone this repository:
```bash
git clone https://github.com/Ryuji-Kishima-Fella/mood-tracker.git
```
3. Open the terminal and navigate to the mood_tracker folder:
```bash
cd mood_tracker
```

4. Run the program:
```bash
pythoon mood_tracker.py
```

## Menu Options
```yaml
=== Mood Tracker ===
1. Log today's mood
2. View mood history
3. View mood summary
4. Export mood history to CSV
5. Exit
``` 


## Example Output
Mood Summary Example:
```yaml
📊 Mood Summary:
  Happy: 5 times
  Stressed: 2 times
  Tired: 1 time

Most frequent mood: 😌 Happy
```
CSV Export Example:
```csv
Date,Mood
2025-11-05 19:28:56, Happy
2025-11-05 22:56:59, Tired
```

## Future Improvements
- Add charts/graphs
- Add daily reminders
- Turn into a web or mobile app

---

## 🕓 Version History

For a full and detailed version history, see
📜 **[CHANGELOG.md](CHANGELOG.md)**

Summary:

v1.x — Console-based implementations and early features

v2.x — GUI-based desktop application with enhanced usability and visualization


---

## Known Issues
- On some systems, keyboard shortcuts may differ by OS
- GUI layout may scale differently on high-DPI displays


---


## 🚀 Release Checklist

1. [ ] Update version number in README and CHANGELOG  
2. [ ] Commit and push changes  
3. [ ] Run `git release vX.Y.Z` (or create tag manually)  
4. [ ] Verify tag appears under [Releases](https://github.com/<your-username>/mood-tracker/releases)

