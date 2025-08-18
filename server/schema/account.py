accountSchema = {
    "username": str,
    "username_lower": str,
    "email": str,
    "email_lower": str,
    "password_hash": str,
}


def validate_profile(profile: dict) -> bool:
    for key, value in accountSchema.items():
        if key not in profile or not isinstance(profile[key], value):
            return False
    return True
