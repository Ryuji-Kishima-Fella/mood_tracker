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

def main():
    print("=== Mood Tracker ===")
    print("1. Log today's mood")
    print("2. View mood history")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        log_mood()
    elif choice == "2":
        show_moods()
    else:
        print("Goodbye!")

if __name__ == "__main__":
    main()
