from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)

# ---------- Home ----------
@app.route("/")
def home():
    return render_template("home.html")

# ---------- Add Expense ----------
@app.route("/add", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        category = request.form["category"]
        amount = request.form["amount"]
        date = request.form["date"]

        file_exists = os.path.isfile("expenses.csv")

        with open("expenses.csv", "a", newline="") as file:
            fieldnames = ["ID", "Category", "Amount", "Date"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            # Auto-generate ID
            next_id = 1
            if os.path.isfile("expenses.csv"):
                with open("expenses.csv", "r") as f:
                    reader = list(csv.DictReader(f))
                    if reader:
                        last_id = int(reader[-1]["ID"])
                        next_id = last_id + 1

            writer.writerow({"ID": next_id, "Category": category, "Amount": amount, "Date": date})

        return redirect("/expenses")

    return render_template("add.html")

# ---------- View Expenses ----------
@app.route("/expenses")
def view_expenses():
    expenses = []
    try:
        with open("expenses.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                expenses.append(row)
    except FileNotFoundError:
        expenses = []

    return render_template("expenses.html", expenses=expenses)

if __name__ == "__main__":
    app.run(debug=True)
