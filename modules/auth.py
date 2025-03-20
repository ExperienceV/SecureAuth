from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Set up security
SECRET_KEY = "ThisIsAVeryUltraSuperIncredibleSecReTKEY"  
ALGORITHM = "HS256" 

# Expiration times
ACCESS_TOKEN_EXPIRE_MINUTES = 15  
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Bearer authentication scheme
security = HTTPBearer()

def create_access_token(data: dict):
    """
    Create a JWT access token.
    - data: Data to include in the token (for example, the username).
    - exp: Token expiration time (15 minutes by default).
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    """
    Create a refresh JWT token.
    - data: Data to include in the token.
    - exp: Token expiration time (7 days by default).
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    """
    Verifies the validity of a JWT token.
    - token: JWT token to verify.
    - Returns the token payload if valid.
    - Throws an HTTP 401 exception if the token is invalid or has expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Gets the current user from the JWT token.
    - credentials: Authentication credentials (Bearer token).
    - Returns the username extracted from the token.
    """
    token = credentials.credentials
    payload = verify_token(token)
    return payload.get("sub")