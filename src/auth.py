import os
from datetime import datetime, timezone, timedelta
import jwt

def get_aut_token(username: str, password: str) -> str:
    token = None
    if username == os.getenv('APP_USERNAME') and password == os.getenv('APP_PASSWORD'):
        now = datetime.now(timezone.utc)
        exp = now + timedelta(hours=1)
        payload = {
            'user': username,
            'role': "ADMIN",
            'iat': now,
            'exp': exp
        }
        token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm="HS256")
    return token

def validate_auth_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
        return payload
    except Exception as ex:
        return None