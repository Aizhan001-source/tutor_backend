<<<<<<< HEAD
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.jwt import decode_access_token

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        payload = decode_access_token(credentials.credentials)
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
=======

>>>>>>> origin/lili
