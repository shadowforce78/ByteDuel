def create_account(db, collection_name, account_data):
    result = db[collection_name].insert_one(account_data)
    return {"inserted_id": str(result.inserted_id)}