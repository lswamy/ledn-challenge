import os
import json
from datetime import datetime
from flask import g
from pymongo import MongoClient, InsertOne, IndexModel, ASCENDING
from pymongo.database import Database

def get_db() -> Database:
    if 'db' not in g:
        mongo_client = MongoClient(os.getenv('MONGODB_URL'), tls=False)
        db = mongo_client[os.getenv('MONGODB_NAME')]
        g.db = db
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(app):
    with app.app_context():
        db = get_db()

        num_docs = db.accounts.count_documents({})
        if num_docs > 0:
            return num_docs

        db.accounts.create_indexes([
            IndexModel([("country", ASCENDING)]),
            IndexModel([("mfa", ASCENDING)]),
            IndexModel([("firstName", ASCENDING), ("lastName", ASCENDING)]),
            IndexModel([("createdDate", ASCENDING)]),
            IndexModel([("amt", ASCENDING)])
        ])

        current_dir = os.path.dirname(os.path.realpath(__file__))
        with open(f"{current_dir}/../accounts_large.json", "r") as f:
            accounts = json.load(f)
            
        account_ops = []
        for account in accounts:
            account['dob'] = datetime.strptime(account.get('dob'), "%Y-%m-%dT%H:%M:%S.%fZ")
            account['createdDate'] = datetime.strptime(account.get('createdDate'), "%Y-%m-%dT%H:%M:%S.%fZ")
            account_ops.append(InsertOne(account))

        batch_size = 1000
        batches = [account_ops[i:i+batch_size] for i in range(0, len(account_ops), batch_size)]
        for batch in batches:
            bulk_result = db.accounts.bulk_write(batch, ordered=False)
            app.logger.info(bulk_result.inserted_count)
