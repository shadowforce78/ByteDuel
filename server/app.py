import os
import fastapi
import dotenv
import pymongo

from service.mongoAction import create_account
from schema.profile import validate_profile

dotenv.load_dotenv()

MONGO_URI = os.getenv("mongo_uri")
KEY = os.getenv("key")

client = pymongo.MongoClient(MONGO_URI)
db = client["ByteDuel"]

app = fastapi.FastAPI()

# tempData = {
#     "username": "JohnDoe",
#     "bio": "Welcome to my profile!",
#     "elo": "Gold",
#     "rank": "Gold"
# }  


@app.get("/")
def read_root():
    return {"message": "Welcome to ByteDuel API"}


@app.post("/create_account")
def create_account_endpoint(account_data: dict, key: str):
    if key != KEY:
        return {"error": "Invalid API key"}
    if not validate_profile(account_data):
        return {"error": "Invalid profile data"}
    return create_account(db, "accounts", account_data)
