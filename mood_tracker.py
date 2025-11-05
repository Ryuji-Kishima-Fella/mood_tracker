from datetime import datetime

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

  
def main():
    print("=== Mood Tracker ===")
    print("1. Log today's mood")
    print("2. View mood history")
    print("3. View mood summary")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        log_mood()
    elif choice == "2":
        show_moods()
    elif choice == "3":
        show_summary()
    else:
        print("Goodbye!")

if __name__ == "__main__":
    main()
