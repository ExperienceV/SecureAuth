from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Configuración de seguridad
SECRET_KEY = "ThisIsAVeryUltraSuperIncredibleSecReTKEY"  
ALGORITHM = "HS256" 

# Tiempos de expiración
ACCESS_TOKEN_EXPIRE_MINUTES = 15  
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Esquema de autenticación Bearer
security = HTTPBearer()

def create_access_token(data: dict):
    """
    Crea un token JWT de acceso.
    - data: Datos a incluir en el token (por ejemplo, el nombre de usuario).
    - exp: Tiempo de expiración del token (15 minutos por defecto).
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    """
    Crea un token JWT de refresco.
    - data: Datos a incluir en el token.
    - exp: Tiempo de expiración del token (7 días por defecto).
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    """
    Verifica la validez de un token JWT.
    - token: Token JWT a verificar.
    - Retorna el payload del token si es válido.
    - Lanza una excepción HTTP 401 si el token es inválido o ha expirado.
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
    Obtiene el usuario actual a partir del token JWT.
    - credentials: Credenciales de autenticación (token Bearer).
    - Retorna el nombre de usuario extraído del token.
    """
    token = credentials.credentials
    payload = verify_token(token)
    return payload.get("sub")