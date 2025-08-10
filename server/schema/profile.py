profileSchema = {
    "username": str,
    "bio": str,
    "elo": int,
    "rank": str
}

def validate_profile(profile: dict) -> bool:
    for key, value in profileSchema.items():
        if key not in profile or not isinstance(profile[key], value):
            return False
    return True
