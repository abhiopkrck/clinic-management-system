from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from backend.security.auth import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def require_role(required_roles: list):
    def role_checker(token: str = Depends(oauth2_scheme)):
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("role_id") not in required_roles:
            raise HTTPException(status_code=403, detail="Access denied")
        return payload
    return role_checker
