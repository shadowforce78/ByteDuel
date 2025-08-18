import os
import secrets
import datetime as dt
import fastapi
import dotenv
import pymongo
import bcrypt
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from service.mongoAction import create_account
from schema.profile import validate_profile

dotenv.load_dotenv()

MONGO_URI = os.getenv("mongo_uri")
KEY = os.getenv("key")

client = pymongo.MongoClient(MONGO_URI)
db = client["ByteDuel"]

app = fastapi.FastAPI()

# Allow CORS for client app (adjust origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/get_account")
def get_account_endpoint(username: str, key: str, email: str, password: str):
    if key != KEY:
        return {"error": "Invalid API key"}
    account = db["accounts"].find_one({"$or": [{"email": email}, {"username": username}]})
    if account and account["password"] == password:
        return account
    return {"error": "Account not found or invalid credentials"}


# ---------- Auth models ----------
class RegisterBody(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class LoginBody(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: str = Field(min_length=6, max_length=128)


def hash_password(pw: str) -> str:
    return bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(pw: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(pw.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


def issue_token(account_id: str) -> str:
    token = secrets.token_urlsafe(32)
    db["auth_tokens"].insert_one({
        "token": token,
        "account_id": account_id,
        "created_at": dt.datetime.utcnow(),
        # Optionally set an expiry, e.g. +30 days
        # "expires_at": dt.datetime.utcnow() + dt.timedelta(days=30),
        "valid": True,
    })
    return token


@app.post("/auth/register")
def register(body: RegisterBody):
    # Normalize
    username = body.username.strip()
    email = body.email.lower().strip()
    # Uniqueness checks
    exists = db["accounts"].find_one({
        "$or": [
            {"email_lower": email},
            {"username_lower": username.lower()},
        ]
    })
    if exists:
        raise fastapi.HTTPException(status_code=400, detail="Username or email already in use")

    doc = {
        "username": username,
        "username_lower": username.lower(),
        "email": body.email,
        "email_lower": email,
        "password_hash": hash_password(body.password),
        "created_at": dt.datetime.utcnow(),
    }
    res = db["accounts"].insert_one(doc)
    account_id = str(res.inserted_id)
    token = issue_token(account_id)
    return {
        "ok": True,
        "key": token,
        "user": {"id": account_id, "username": username, "email": body.email},
    }


@app.post("/auth/login")
def login(body: LoginBody):
    query = None
    if body.email:
        query = {"email_lower": body.email.lower().strip()}
    elif body.username:
        query = {"username_lower": body.username.lower().strip()}
    else:
        raise fastapi.HTTPException(status_code=400, detail="Email or username is required")

    account = db["accounts"].find_one(query)
    if not account or not verify_password(body.password, account.get("password_hash", "")):
        raise fastapi.HTTPException(status_code=401, detail="Invalid credentials")

    account_id = str(account["_id"])  # ObjectId -> str
    token = issue_token(account_id)
    return {
        "ok": True,
        "key": token,
        "user": {"id": account_id, "username": account.get("username"), "email": account.get("email")},
    }


class ValidateBody(BaseModel):
    key: str = Field(min_length=10)


@app.post("/auth/validate")
def validate(body: ValidateBody):
    tok = db["auth_tokens"].find_one({"token": body.key, "valid": True})
    if not tok:
        raise fastapi.HTTPException(status_code=401, detail="Invalid token")
    # Optional expiry check if you add expires_at
    # if tok.get("expires_at") and tok["expires_at"] < dt.datetime.utcnow():
    #     raise fastapi.HTTPException(status_code=401, detail="Token expired")

    acc = db["accounts"].find_one({"_id": tok["account_id"]})
    # account_id stored as str; ensure lookup supports str/ObjectId
    if not acc:
        try:
            from bson import ObjectId
            acc = db["accounts"].find_one({"_id": ObjectId(tok["account_id"])})
        except Exception:
            acc = None
    if not acc:
        raise fastapi.HTTPException(status_code=401, detail="Account not found for token")
    return {
        "ok": True,
        "user": {"id": str(acc.get("_id")), "username": acc.get("username"), "email": acc.get("email")},
    }


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    # Transform FastAPI's default validation error into simpler list
    simplified = []
    for err in exc.errors():
        loc = ".".join(str(x) for x in err.get("loc", []) if x not in ("body",))
        simplified.append(f"{loc}: {err.get('msg')}")
    return JSONResponse(
        status_code=422,
        content={
            "ok": False,
            "error": "Validation failed",
            "errors": simplified,
        },
    )