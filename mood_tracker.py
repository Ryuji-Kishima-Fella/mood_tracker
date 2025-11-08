from datetime import datetime
import csv
import sys

def log_mood():
    mood = input("How are you feeling today? ")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("mood_log.txt", "a") as file:
        file.write(f"{date} - {mood}\n")

    print("✅ Mood saved successfully!")

def show_moods():
    try:
        with open("mood_log.txt", "r") as file:
            print("\n📘 Your Mood History:\n")
            print(file.read())
    except FileNotFoundError:
        print("No mood records found yet. Start by logging your first mood!")

def show_summary():
    try:
        with open("mood_log.txt", "r") as file:
            moods = [line.split("-")[1].strip().lower() for line in file]
            total = len(moods)

            if total == 0:
                print("No mood records found yet.")
                return

            unique_moods = {}
            for mood in moods:
                unique_moods[mood] = unique_moods.get(mood, 0) + 1
            
            print("\n📊 Mood Summary:")
            for mood, count in unique_moods.items():
                print(f"    {mood.capitalize()}: {count} times")

            most_common = max(unique_moods, key=unique_moods.get)
            print(f"\nMost frequent mood: 😌 {most_common.capitalize()}")
    except FileNotFoundError:
        print("No mood records found yet. Start by logging your first mood!")

def view_by_date():
    # Display moods logged on a specific date.
    try:
        target_date = input("Enter data (YYYY-MM-DD): ").strip()
        # Validate date format
        datetime.strptime(target_date, "%Y-%m-%d")

        with open("mood_log.txt", "r") as file:
            found = False
            print(f"\n📅 Moods on {target_date}:")
            for line in file:
                if line.startswith(target_date):
                    print(" ", line.strip())
                    found = True
            if not found:
                print("No moods found for that date.")
    except ValueError:
        print("❌ Invalid date format. Please use YYYY-MM-DD")
    except FileNotFoundError:
        print("⚠️ No mood records found yet.")

def export_to_csv():
    # Export all mood entries from mood_log.txt into mood_log.csv
    try:
        with open("mood_log.txt", "r") as infile, open("mood_log.csv", "w", newline="", encoding="utf-8") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["Date", "Mood"]) # Header row
            for line in infile:
                parts = line.strip().split(" - ")
                if len(parts) == 2:
                    writer.writerow(parts)
        
        print("✅ Mood history exported to mood_log.csv successfully!")
    except FileNotFoundError:
        print("⚠️ No mood records found yet. Please log some moods first.")

def delete_last_entry():
    # Remove the last mood entry from mood_log.txt.
    try:
        with open("mood_log.txt", "r") as file:
            lines = file.readlines()
        if not lines:
            print("⚠️ No entries to delete.")
            return

        print(f"Last entry:\n{lines[-1].strip()}")
        confirm = input("Delete this entry? (Y/N): ").strip().lower()
        if confirm == "y":
            with open("mood_log.txt", "w") as file:
                file.writelines(lines[:-1])
            print("🗑️ Last entry deleted.")
        else:
            print("❌ Deletion cancelled.")
    except FileNotFoundError:
        print("⚠️ No mood records found yet.")
  
def edit_mood_entry():
    # Allow user to edit a specific mood entry.
    try:
        with open("mood_log.txt", "r") as file:
            lines = file.readlines()

        if not lines:
            print("⚠️ No mood entries found.")
            return

        # Display entries with line numbers
        print("\n📝 Mood History:")
        for i, line in enumerate(lines, start=1):
            print(f"{i}.{line.strip()}")

        # Ask user which entry to edit
        index = input("Enter the number of the entry to edit: ").strip()
        if not index.isdigit():
            print("❌ Invalid input. Please enter a number.")
            return

        index = int(index)
        if index < 1 or index > len(lines):
            print("❌ Invalid entry number.")
            return

        # Show the selected entry
        old_entry = lines[index - 1].strip()
        print(f"\nCurrent entry: {old_entry}")

        # Ask for new mood
        new_mood = input("Enter new mood: ").strip().capitalize()
        if not new_mood:
            print("❌ Mood entry cannot be empty.")
            return

        # Extract date part and replace mood
        if " - " in old_entry:
            date_part = old_entry.split(" - ")[0]
            new_entry = f"{date_part} - {new_mood}\n"
        else:
            new_entry = f"{new_entry}\n"

        # Replace and save
        lines[index - 1] = new_entry
        with open("mood_log.txt", "w") as file:
            file.writelines(lines)

        print(f"✅ Entry updated: {new_entry.strip()}")

    except FileNotFoundError:
        print("⚠️ No mood records found yet.")

def main():
    
    while True:
        print("\n=== Mood Tracker ===")
        print("1. Log today's mood")
        print("2. View mood history")
        print("3. View mood summary")
        print("4. View moods by date")
        print("5. Export mood history to CSV.")
        print("6. Delete last mood entry")
        print("7. Edit a mood entry")
        print("X. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            log_mood()
        elif choice == "2":
            show_moods()
        elif choice == "3":
            show_summary()
        elif choice == "4":
            view_by_date()
        elif choice =="5":
            export_to_csv()
        elif choice == "6":
            delete_last_entry()
        elif choice == "7":
            edit_mood_entry()
        elif choice == "x":
            print("Goodbye!")
            break 
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
