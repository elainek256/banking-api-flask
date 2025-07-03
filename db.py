import sqlite3

customers = {}      # customer_id = customer data
accounts = {}       # account_id = account data
transactions = []   # list of transaction dictionary

#for auto-increase
next_customer_id = 1
next_account_id = 1001
next_transaction_id = 1
