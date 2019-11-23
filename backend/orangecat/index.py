from flask import Flask, jsonify, request

from cashman.model.expense import Expense, ExpenseSchema
from cashman.model.income import Income, IncomeSchema
from cashman.model.transaction_type import TransactionType

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello world!'


if __name__ == "__main__":
    app.run()
