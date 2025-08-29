import sqlite3
import csv

# Create table if it doesn't exist
def create_table():
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    category TEXT,
                    amount REAL,
                    description TEXT)''')
    conn.commit()
    conn.close()

# Add expense
def add_expense(date, category, amount, description):
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
                (date, category, amount, description))
    conn.commit()
    conn.close()
    print("✅ Expense added successfully!")

# View all expenses
def view_expenses():
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses")
    rows = cur.fetchall()
    conn.close()
    
    if len(rows) == 0:
        print("No expenses found.")
    else:
        print("\nAll Expenses:")
        print("ID | Date       | Category   | Amount | Description")
        print("-"*50)
        for row in rows:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}")

# Delete expense by ID
def delete_expense(expense_id):
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()
    print(f"🗑 Expense with ID {expense_id} deleted.")

# Summary report (total spent by category)
def summary_report():
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    rows = cur.fetchall()
    conn.close()
    
    if len(rows) == 0:
        print("No expenses found.")
    else:
        print("\nSummary Report (Category-wise total):")
        for row in rows:
            print(f"{row[0]} : {row[1]}")

# Search expenses by date or category
def search_expenses():
    print("\nSearch Expenses")
    print("1. By Date")
    print("2. By Category")
    choice = input("Enter your choice: ")

    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()

    if choice == "1":
        date = input("Enter date (YYYY-MM-DD): ")
        cur.execute("SELECT * FROM expenses WHERE date=?", (date,))
    elif choice == "2":
        category = input("Enter category: ")
        cur.execute("SELECT * FROM expenses WHERE category=?", (category,))
    else:
        print("Invalid choice")
        conn.close()
        return

    results = cur.fetchall()
    if results:
        print("\nSearch Results:")
        for row in results:
            print(row)
    else:
        print("No matching expenses found.")

    conn.close()

# Update expense
def update_expense():
    expense_id = input("Enter the ID of the expense to update: ")

    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM expenses WHERE id=?", (expense_id,))
    row = cur.fetchone()
    if not row:
        print("Expense not found.")
        conn.close()
        return

    print(f"Current Record: {row}")
    date = input("Enter new date (YYYY-MM-DD): ")
    category = input("Enter new category: ")
    amount = float(input("Enter new amount: "))
    description = input("Enter new description: ")

    cur.execute("UPDATE expenses SET date=?, category=?, amount=?, description=? WHERE id=?",
                (date, category, amount, description, expense_id))

    conn.commit()
    conn.close()
    print("✅ Expense updated successfully!")

# Export expenses to CSV
def export_to_csv():
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses")
    rows = cur.fetchall()

    with open("expenses_export.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Date", "Category", "Amount", "Description"])
        writer.writerows(rows)

    conn.close()
    print("📂 Expenses exported to expenses_export.csv")

# ----------------- MAIN MENU -----------------
def main():
    create_table()
    while True:
        print("\n===== Expense Tracker =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Summary Report")
        print("5. Search Expenses")
        print("6. Update Expense")
        print("7. Export Expenses to CSV")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            date = input("Enter date (YYYY-MM-DD): ")
            category = input("Enter category: ")
            amount = float(input("Enter amount: "))
            description = input("Enter description: ")
            add_expense(date, category, amount, description)

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            expense_id = int(input("Enter ID of expense to delete: "))
            delete_expense(expense_id)

        elif choice == "4":
            summary_report()

        elif choice == "5":
            search_expenses()

        elif choice == "6":
            update_expense()

        elif choice == "7":
            export_to_csv()

        elif choice == "8":
            print("Exiting... Goodbye 👋")
            break

        else:
            print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    main()


