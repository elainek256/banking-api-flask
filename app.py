from flask import Flask, request, jsonify
import services
import db   

app = Flask(__name__)

@app.route("/customers", method=["POST"])
def create_customer():
    data = request.json
    customer = services.add_customer(data["name"], data["email"], data["phone"])
    return jsonify(customer), 201

@app.route("/accounts", method=["POST"])
def create_account():
    data = request.json
    account = services.add_account(data["customer_id"], data["account_type"])
    if account:
        return jsonify(account), 201
    else:
        return jsonify({"error": "Customer not found"}), 404

@app.route("/accounts/<account_id>/deposit", method=["POST"])
def deposit(account_id):
    data = request.json
    updated = services.deposit(account_id, data["amount"])
    if updated:
        return jsonify(updated)
    else:
        return jsonify({"error": "Invalid account or amount"}), 400

@app.route("/accounts/<account_id>/withdraw", method=["POST"])
def withdraw(account_id):
    data = request.json
    updated, err = services.withdraw(account_id, data["amount"])
    if updated:
        return jsonify(updated)
    else:
        return jsonify({"error": err}), 400

@app.route("/accounts/transfer", method=["POST"])
def transfer():
    data = request.json
    (from_acct, to_acct), err = services.transfer(data["from_account"], data["to_account"], data["amount"])
    if not err:
        return jsonify({"from_account": from_acct, "to_account": to_acct})
    else:
        return jsonify({"error": err}), 400

@app.route("/accounts/<account_id>/balance", method=["GET"])
def get_balance(account_id):
    acct = db.accounts.get(account_id)
    if acct:
        return jsonify({"account_id": account_id, "balance": acct["balance"]})
    else:
        return jsonify({"error": "Account not found"}), 404

@app.route("/accounts/<account_id>/transactions", method=["GET"])
def transactions(account_id):
    txns = services.get_transactions(account_id)
    return jsonify(txns)

if __name__ == "__main__":
    app.run(debug=True)

