from passlib.context import CryptContext
from jose import jwt
import datetime
from typing import Union
from typing import List, Callable, Dict, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError

SECRET_KEY="f3a9c8d4e2b1a7c9d8f4e6a2b7c9d1f3a8e4b6c7d9f2a3b5c7d8e9f1a2b3c4d5"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    if len(password) > 72:
        password = password[:72]
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Union[datetime.timedelta, None] = None) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + (expires_delta or datetime.timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


security = HTTPBearer()

def decode_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if "roles" not in payload:
            raise JWTError("Token missing roles")
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

def get_current_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header")
    return decode_token(credentials.credentials)

def has_any_role(allowed_roles: List[str]) -> Callable[..., Dict[str, Any]]:
    def role_checker(payload: Dict[str, Any] = Depends(get_current_token)) -> Dict[str, Any]:
        token_roles = payload.get("roles")

        print("DEBUG roles:", token_roles, type(token_roles))  # 👈 keep this for now

        if not token_roles:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing roles"
            )

        if isinstance(token_roles, str):
            import ast
            try:
                token_roles = ast.literal_eval(token_roles)  
            except:
                token_roles = [token_roles]

        
        if not isinstance(token_roles, list):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid roles format"
            )

        if not set(token_roles).intersection(set(allowed_roles)):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: insufficient role"
            )

        return payload

    return role_checker
