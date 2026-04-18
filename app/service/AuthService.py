# app/service/AuthService.py
from passlib.context import CryptContext
from jose import jwt, JWTError
import datetime
from typing import Union, List, Callable, Dict, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = "f3a9c8d4e2b1a7c9d8f4e6a2b7c9d1f3a8e4b6c7d9f2a3b5c7d8e9f1a2b3c4d5"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def get_password_hash(password: str) -> str:
    # bcrypt only supports up to 72 bytes
    if len(password.encode("utf-8")) > 72:
        raise HTTPException(status_code=400, detail="Password too long (max 72 bytes)")
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: dict, expires_delta: Union[datetime.timedelta, None] = None
) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + (
        expires_delta or datetime.timedelta(minutes=15)
    )
    to_encode.update({"exp": expire})

    roles = to_encode.get("roles")
    if roles:
        if isinstance(roles, str):
            to_encode["roles"] = [roles]
        elif not isinstance(roles, list):
            raise ValueError("Roles must be string or list")

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if "roles" not in payload:
            raise JWTError("Token missing roles")
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )


def get_current_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Dict[str, Any]:
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
        )
    return decode_token(credentials.credentials)


def has_any_role(allowed_roles: List[str]) -> Callable[..., Dict[str, Any]]:
    def role_checker(
        payload: Dict[str, Any] = Depends(get_current_token),
    ) -> Dict[str, Any]:
        token_roles = payload.get("roles")
        if not token_roles:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing roles"
            )

        if isinstance(token_roles, str):
            token_roles = [token_roles]
        if not isinstance(token_roles, list):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid roles format"
            )

        if not any(role in allowed_roles for role in token_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: insufficient role",
            )

        return payload

    return role_checker
