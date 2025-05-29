from flask import Flask,render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
#from app import  db

# The `project_dir` variable is being used to store the absolute path of the directory where the
# current Python script is located. This can be useful for referencing files or resources within the
# project directory, such as templates, static files, or database files. In this specific code
# snippet, it is being used to set the project directory for the Flask application.
project_dir = os.path.dirname(os.path.abspath(__file__))
# The line `database_file ="sqlite:///{}".format( os.path.join(project_dir, 'expense.db'))` is
# constructing a SQLite database file path.
database_file ="sqlite:///{}".format( os.path.join(project_dir, 'expense.db'))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
db = SQLAlchemy(app)


class Expense(db.Model):
  id = db.Column(db.Integer,primary_key=True)
  date = db.Column(db.String(100), nullable=False)
  expensename = db.Column(db.String(100), nullable=False)
  amount= db.Column(db.Integer, nullable=False)
  category = db.Column(db.String(100), nullable=False)
  
@app.route('/')
def add():
  return render_template('add.html')



@app.route('/expenses')
def expenses():
  # `expenses = Expense.query.all()` is a SQLAlchemy query that retrieves all the records from the
  # `Expense` table in the database. It fetches all the rows from the `Expense` table and stores them
  # in the `expenses` variable as a list of `Expense` objects.
  expenses = Expense.query.all()
  
  # The lines `total = 0`, `t_business = 0`, `t_food = 0`, `t_entertainment = 0`, `t_transport = 0`,
  # and `t_others = 0` are initializing variables to store the total amount spent in different
  # categories.
  total = 0
  t_business = 0
  t_food = 0
  t_entertainment = 0
  t_transport = 0
  t_business
  t_utilities = 0
  t_others = 0
  
  # The code snippet `for expense in expenses: total += expense.amount` is iterating over each
  # `Expense` object in the `expenses` list retrieved from the database query. For each `Expense`
  # object, it is adding the `amount` attribute of that expense to the `total` variable. This
  # effectively calculates the total amount spent across all expenses in the database.
  for expense in expenses:
    total += expense.amount
    if expense.category == 'Business':
      t_business += expense.amount
    elif expense.category == 'Food':
        t_food += expense.amount 
    elif expense.category == 'Entertainment':
        t_entertainment += expense.amount
    elif expense.category == 'Transport':
        t_transport += expense.amount
    elif expense.category == 'Others':
        t_others += expense.amount
    elif expense.category == 'Utilities':
        t_utilities += expense.amount
        
    elif expense.category.lower() in ['others', 'other']:
      t_others += expense.amount
      
  return render_template('expenses.html', expenses=expenses,              total=total,t_business=t_business, t_food=t_food, t_entertainment =t_entertainment, t_transport=t_transport, t_utilities = t_utilities, t_others=t_others)

@app.route('/delete/<int:id>')
def delete(id):
  
    expense = Expense.query.filter_by(id = id).first()
    db.session.delete(expense)
    db.session.commit()
    return redirect('/expenses')

@app.route('/updateexpense/<int:id>')
def updateexpense(id):
  expense = Expense.query.filter_by(id=id).first()
  return render_template('updateexpense.html', expense=expense)

@app.route('/edit' , methods=['POST'])
def edit():
  id = request.form['id']
  date = request.form['date']
  expensename = request.form['expensename']
  amount = request.form['amount']
  category = request.form['category']
  
  expense = Expense.query.filter_by(id=id).first()
  expense.date = date
  expense.expensename = expensename
  expense.amount = amount
  expense.category = category
  
  db.session.commit()
  
  return redirect('/expenses')
  

@app.route('/addexpense', methods=['POST'])
def addexpense():
  date = request.form['date']
  expensename = request.form['expensename']
  amount = request.form['amount']
  category = request.form['category']
  expense = Expense(date=date, expensename=expensename, amount=amount, category=category)
  db.session.add(expense)
  db.session.commit()
  return redirect("/expenses")
  
if __name__ == '__main__':
  with app.app_context():
        db.create_all()
  app.run(debug=True)