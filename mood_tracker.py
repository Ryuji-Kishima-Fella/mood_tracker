from datetime import datetime
import csv


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
        with open("mood_log.txt", "r") as file:
            found = False
            print(f"\n📅 Moods on {target_date}:")
            for line in file:
                if line.startswith(target_date):
                    print("", line.strip())
                    found = True
            if not found:
                print("No moods found for that date.")
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

  
def main():
    print("=== Mood Tracker ===")
    print("1. Log today's mood")
    print("2. View mood history")
    print("3. View mood summary")
    print("4. View moods by date")
    print("5. Export mood history to CSV.")
    print("X. Exit")

    choice = input("Enter your choice: ")

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
    else:
        print("Goodbye!")

if __name__ == "__main__":
    main()
