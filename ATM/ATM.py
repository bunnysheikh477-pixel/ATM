import os
import signal
from flask import Flask, render_template, request, jsonify,session

app = Flask(__name__)

balance = 100.0 


@app.route('/')
def home():
    return render_template("ATM.html", balance=balance)


# Deposit
@app.route('/deposite', methods=['POST'])
def deposite():
    global balance
    try:
        amount = float(request.form['amount'])
        phone = request.form.get('phone')
        password = request.form.get('password')
        if amount <= 0:
            return render_template("ATM.html", balance=balance, message="Invalid amount! Please enter a positive number.")
        
        balance += amount
        return render_template("ATM.html", balance=balance, message=f"Deposit Successful: {amount:.2f}")
    except ValueError:
        return render_template("ATM.html", balance=balance, message="Error: Please enter a valid number.")


# Withdraw
@app.route('/withdraw', methods=['POST'])
def withdraw():
    global balance
    try:
        amount = float(request.form['amount'])
        phone = request.form.get('phone')
        password = request.form.get('password')

        if amount <= 0:
            return render_template("ATM.html", balance=balance, message="Invalid amount! Please enter a positive number.")
        elif amount > balance:
            return render_template("ATM.html", balance=balance, message="Insufficient funds!")

        # If you want, you can check phone & password later (for now ignored)
        balance -= amount
        return render_template("ATM.html", balance=balance, message=f"Withdraw Successful: {amount:.2f}")
    except ValueError:
        return render_template("ATM.html", balance=balance, message="Error: Please enter a valid number.")


# Transfer
@app.route('/transfer', methods=['POST'])
def fast_transfer():
    global balance
    try:
        amount = float(request.form['amount'])
        if amount <= 0:
            return render_template("ATM.html", balance=balance, message="Invalid amount! Please enter a positive number.")
        elif amount>50000:
            return render_template("ATM.html" ,balance=balance,message="Transaction is not greater than 40000:")
        elif amount > balance:
            return render_template("ATM.html", balance=balance, message="Insufficient funds!")

        balance -= amount
        balance -= 20
        return render_template("ATM.html",balance=balance, message=f"Using Fast Transfer 20 Rs is charged")
        return render_template("ATM.html", balance=balance, message=f"Transfer Successful: {amount:.2f}")
    except ValueError:
        return render_template("ATM.html", balance=balance, message="Error: Please enter a valid number.")


# Funds Donation
@app.route('/funds', methods=['POST'])
def funds():
    global balance
    try:
        amount = float(request.form['amount'])
        company = request.form.get('company')
        phone = request.form.get('phone')

        
        
        if amount <= 0:
            return render_template("ATM.html", balance=balance, message="Invalid amount! Please enter a positive number.")
        elif amount>40000:
            return render_template("ATM.html" ,balance=balance,message="Transaction is not greater than 40000:")
        elif amount > balance:
            return render_template("ATM.html", balance=balance, message="Insufficient funds!")

        balance -= amount
        return render_template("ATM.html", balance=balance, message=f"Donation Successful: {amount:.2f}")
    except ValueError:
        return render_template("ATM.html", balance=balance, message="Error: Please enter a valid number.")


# API for balance (for JS fetch)
@app.route('/api/balance/<user>', methods=['GET'])
def api_balance(user):
    return jsonify({"user": user, "balance": balance})


@app.route('/exit', methods=['POST'])
def exit_app():
    func = request.environ.get('werkzeug.server.shutdown')
    if func:
        func()   # this stops theFlask server
    
    return "ATM closed. Goodbye!"

if __name__ == "__main__":
    app.run(debug=True)
