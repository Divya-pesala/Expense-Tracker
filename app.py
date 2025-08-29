from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello Divya, Expense Tracker is running in Flask!"

if __name__ == "__main__":
    app.run(debug=True)
@app.route('/expenses')
def view_expenses():
    expenses = []
    try:
        with open('expenses.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                expenses.append(row)
    except FileNotFoundError:
        expenses = []

    return render_template("expenses.html", expenses=expenses)
