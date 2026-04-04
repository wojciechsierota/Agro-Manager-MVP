import reports
import ai_advisor


def main_menu():
    print("\n" + "="*30)
    print("     AGRO MANAGER MVP 1.0")
    print("=" * 30)
    print(f"""1. Get Field Summary
2. Show Costs Report 
3. Add New Field
4. Add New Operation
5. Add New Sale
6. Update Operation Cost
7. Update Current Crop
8. Delete Field
9. Delete Operation
10. Ask AI Advisor
11. Show Financial Balance
12. Export Financial Report
13. Exit
        """)

    choice = input("\nChoose an option: ")
    if choice == '1':
        reports.get_field_summary()
    elif choice == '2':
        reports.get_costs_report()
    elif choice == '3':
        reports.add_new_field()
    elif choice == '4':
        reports.add_operations()
    elif choice == '5':
        reports.add_sale()
    elif choice == '6':
        reports.update_operation_cost()
    elif choice == '7':
        reports.update_current_crop()
    elif choice == '8':
        reports.delete_field()
    elif choice == '9':
        reports.delete_operations()
    elif choice == '10':
        ai_advisor.ask_ai_advisor()
    elif choice == '11':
        reports.get_financial_report() 
    elif choice == '12':
        reports.export_financial_report()   
    elif choice == '13':
        print("Closing the system... Goodbye!")
        exit()
    else:
        print("Invalid choice, try again.")


if __name__ == "__main__":
    while True:
        main_menu()
