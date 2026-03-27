import reports
import ai_advisor


def main_menu():
    print("\n" + "="*30)
    print("     AGRO MANAGER MVP 1.0")
    print("=" * 30)
    print(f"""1. Show Costs Report 
2. Add New Field
3. Add New Operation
4. Update Operation Cost
5. Delete Field
6. Delete Operation
7. Ask AI Advisor
8. Show Financial Balance
9. Exit
        """)

    choice = input("\nChoose an option: ")

    if choice == '1':
        reports.get_costs_report()
    elif choice == '2':
        reports.add_new_field()
    elif choice == '3':
        reports.add_operations()
    elif choice == '4':
        reports.update_operation_cost()
    elif choice == '5':
        reports.delete_field()
    elif choice == '6':
        reports.delete_operations()
    elif choice == '7':
        ai_advisor.ask_ai_advisor()
    elif choice == '8':
        reports.get_financial_report()    
    elif choice == '9':
        print("Closing the system... Goodbye!")
        exit()
    else:
        print("Invalid choice, try again.")


if __name__ == "__main__":
    while True:
        main_menu()
