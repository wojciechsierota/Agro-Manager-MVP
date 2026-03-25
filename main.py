import reports
import ai_advisor


def main_menu():
    print("\n" + "="*30)
    print("AGRO MANAGER MVP 1.0")
    print("=" * 30)
    print("1. View Cost Report (SQL)")
    print("2. Ask AI Agronomist (Gemini)")
    print("3. Exit")

    choice = input("\nChoose an option: ")

    if choice == '1':
        reports.get_costs_report()
    elif choice == '2':
        question = input("Your question to AI: ")
        print(ai_advisor.ask_ai_advisor(question))
    elif choice == '3':
        print("Goodbye!")
        exit()
    else:
        print("Invalid choice, try again.")


if __name__ == "__main__":
    while True:
        main_menu()
