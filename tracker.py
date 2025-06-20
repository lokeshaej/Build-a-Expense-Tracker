import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

CSV_FILE = "expensesss.csv"

def load_expenses():
    return pd.read_csv(CSV_FILE)

def save_expenses(expenses):
    expenses.to_csv(CSV_FILE, index=False)

def spendingoverview(expenses):
    print("\n--- Spending Overview ---")
    print(expenses)
    print(f"\nTotal Amount Spent Overall: ₹{np.sum(expenses['Amount'])}")
    print(f"\nHighest Expense Entry:\n{expenses.loc[expenses['Amount'].idxmax()]}")
    print(f"\nLowest Expense Entry:\n{expenses.loc[expenses['Amount'].idxmin()]}")

def categorywiseanalysis(expenses):
    category_summary = expenses.groupby('Category')['Amount'].agg(['sum', 'count'])
    category_summary.rename(columns={'sum': 'Total Amount', 'count': 'Transaction Count'}, inplace=True)
    total_overall_spent = np.sum(expenses['Amount'])
    category_summary['Percentage of Total'] = (category_summary['Total Amount'] / total_overall_spent * 100).round(2)
    
    print("\n--- Category-Wise Analysis ---")
    print(category_summary.to_string(float_format="%.2f"))

def piechart(expenses):
    category_summary = expenses.groupby('Category')['Amount'].sum()
    total = category_summary.sum()
    if total == 0:
        print("No expenses to show in pie chart.")
        return

    plt.figure(figsize=(8, 6))
    plt.pie(category_summary, labels=category_summary.index, autopct='%1.1f%%')
    plt.title('Expense Distribution by Category')
    plt.axis('equal')
    plt.show()

def addnewexpense(expenses):
    while True:
        date_str = input("Enter Date (DD/MM/YYYY): ").strip()
        try:
            new_date = datetime.strptime(date_str, '%d/%m/%Y').date()
            break
        except ValueError:
            print("Invalid date format. Please use DD/MM/YYYY.")
    
    category = input("Enter Category: ").strip()
    while not category:
        print("Category cannot be empty.")
        category = input("Enter Category: ").strip()

    while True:
        try:
            amount = float(input("Enter Amount: ").strip())
            if amount <= 0:
                print("Amount must be positive.")
            else:
                break
        except ValueError:
            print("Invalid amount. Please enter a number.")
    
    description = input("Enter Description: ").strip()

    new_expense = pd.DataFrame([{
        'Date': new_date,
        'Category': category,
        'Amount': amount,
        'Description': description
    }])

    updated_expenses = pd.concat([expenses, new_expense], ignore_index=True)
    save_expenses(updated_expenses)
    print("Expense added successfully!")
    return updated_expenses

def main():
    print("Welcome to the Command-Line Expense Tracker!")

    if not pd.io.common.file_exists(CSV_FILE):
        # Create file with correct headers if it doesn't exist
        pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description']).to_csv(CSV_FILE, index=False)

    expenses = load_expenses()

    while True:
        print("\n--- Main Menu ---")
        print("1. Add New Expense")
        print("2. Spending Overview")
        print("3. Category-wise Overview")
        print("4. Pie Chart View")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            expenses = addnewexpense(expenses)
        elif choice == '2':
            spendingoverview(expenses)
        elif choice == '3':
            categorywiseanalysis(expenses)
        elif choice == '4':
            piechart(expenses)
        elif choice == '5':
            print("Exiting Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
