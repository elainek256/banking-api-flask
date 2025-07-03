import sites
import db

def add_customer(name, email, phone):
    cid = str(db.next_customer_id)
    customer = sites.create_customer(cid, name, email, phone)
    db.customers[cid] = customer
    db.next_customer_id += 1
    return customer

def add_account(customer_id, account_type):
    if customer_id not in db.customers:
        return None
    aid = str(db.next_account_id)
    account = sites.create_account(aid, customer_id, account_type)
    db.accounts[aid] = account
    db.next_account_id += 1
    return account

def deposit(account_id, amount):
    if account_id not in db.accounts:
        return None
    db.accounts[account_id]["balance"] += amount
    txn = sites.create_transaction(db.next_transaction_id, account_id, "deposit", amount)
    db.transactions.append(txn)
    db.next_transaction_id += 1
    return db.accounts[account_id]

def withdraw(account_id, amount):
    if account_id not in db.accounts or amount <= 0:
        return None, "Invalid account or amount"
    if db.accounts[account_id]["balance"] < amount:
        return None, "Insufficient funds"
    db.accounts[account_id]["balance"] -= amount
    txn = sites.create_transaction(db.next_transaction_id, account_id, "withdrawal", amount)
    db.transactions.append(txn)
    db.next_transaction_id += 1
    return db.accounts[account_id], None

def transfer(from_id, to_id, amount):
    if from_id not in db.accounts or to_id not in db.accounts or amount <= 0:
        return None, "Invalid accounts or amount"
    if db.accounts[from_id]["balance"] < amount:
        return None, "Insufficient funds"
    db.accounts[from_id]["balance"] -= amount
    db.accounts[to_id]["balance"] += amount
    txn_out = sites.create_transaction(db.next_transaction_id, from_id, "transfer_out", amount)
    db.next_transaction_id += 1
    txn_in = sites.create_transaction(db.next_transaction_id, to_id, "transfer_in", amount)
    db.next_transaction_id += 1
    db.transactions.extend([txn_out, txn_in])
    return (db.accounts[from_id], db.accounts[to_id]), None

def get_transactions(account_id):
    return [txn for txn in db.transactions if txn["account_id"] == account_id]
