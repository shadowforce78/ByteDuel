accountSchema = {
    "username": str,
    "username_lower": str,
    "email": str,
    "email_lower": str,
    "password_hash": str,
}


def validate_account(account: dict) -> bool:
    for key, value in accountSchema.items():
        if key not in account or not isinstance(account[key], value):
            return False
    return True
