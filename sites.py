from datetime import datetime

def create_customer(customer_id, name, email, phone):
    return {
        "customer_id": customer_id,
        "name": name,
        "email": email,
        "phone": phone
    }

def create_account(account_id, customer_id, account_type):
    return {
        "account_id": account_id,
        "customer_id": customer_id,
        "account_type": account_type,
        "balance": 0.0
    }

def create_transaction(transaction_id, account_id, txn_type, amount):
    return {
        "transaction_id": transaction_id,
        "account_id": account_id,
        "type": txn_type,
        "amount": amount,
        "timestamp": datetime.now().isoformat()
    }